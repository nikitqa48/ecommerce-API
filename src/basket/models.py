from django.db import models
from django.contrib.auth import get_user_model
from .managers import OpenBasketManager, SavedBasketManager
from src.catalogue.models import Product, Stock
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils.timezone import now

from decimal import Decimal as D

class Basket(models.Model):
    """Корзина"""
    #TODO что привязать к корзине, продукт или класс продукта?
    #TODO def remove_product():
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    """Если поле Owner пустое, значит корзина анонимная. После того, как пользователь зайдет в систему - корзины соединятся"""
    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")    
    STATUS_CHOICES = (
        (OPEN, "Open - currently active"),
        (MERGED, "Merged - superceded by another basket"),
        (SAVED, "Saved - for items to be purchased later"),
        (FROZEN, "Frozen - the basket cannot be modified"),
        (SUBMITTED, "Submitted - has been ordered at the checkout"),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=OPEN)
    """Статус, в котором находится корзина."""
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_merged = models.DateTimeField("Дата объединения", null=True, blank=True)
    date_submitted = models.DateTimeField("Дата отправки", null=True,blank=True)
    editable_statuses = (OPEN, SAVED)
    open = OpenBasketManager()
    saved = SavedBasketManager()
    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        """Создаем копию экземпляра корзины"""
        super().__init__(*args, **kwargs)
        self._lines = None

    def __str__(self):
        return f"Владелец - {self.owner}, статус: {self.status}"

    # ========
    # Strategy
    # ========
      
    @property
    def has_strategy(self):
        return hasattr(self, '_strategy')

    @property
    def num_lines(self):
        return self.all_lines().count()
    
    @property
    def is_empty(self):
        return self.id == None and self.num_lines == None

    @property
    def num_items(self):
        return self.all_lines().count()

    def all_lines(self):
        """Возвращает все линии корзины"""
        if self.id is None:
            return self.lines.none()
        if self._lines is None:
            self._lines = (
                self.lines.select_related('product').prefetch_related('product__images')
        )
        return self._lines

    def flash(self):
        """Удалить все линии из корзины"""
        if self.status == self.FROZEN:
            raise PermissionDenied('Замороженная корзина не может быть заморожена')
        self.lines.all().delete()
        self._lines = None

    def get_stock_info(self, product):
        """Кол-во продукта на складе"""
        try:
            stock = Stock.objects.get(product=product)
            return stock.quantity
        except Stock.DoesNotExist:
            return 0

    def merge(self, basket, add_quaintity=True):
        """создать таблицу из кэша корзину"""
        for line_to_merge in basket.lines.all():
            self.merge_line(line_to_merge, add_quaintity)
        basket.status = self.MERGED
        basket.date_merged = now()
        basket._lines = None
        basket.save()

    def merge_line(self, line, add_quantities=1):
        """кэшировать линию корзины в таблицу"""
        try:
            existing_line = self.lines.get(id=line.id)
        except ObjectDoesNotExist:
            line.basket = self
            line.save()
        existing_line.save()

    def add_product(self, product, quantity=1):
        """Добавить продукт"""
        #TODO Если на складе не хватает продуктов, то выдавать ошибку (нет на складе)
        if not self.id:
            self.save()
        stock_info = self.get_stock_info(product)
        if stock_info > 0:
            line, created = self.lines.get_or_create(product=product)
            line.quantity = max(0, line.quantity + quantity)
            line.save()
            return line,created

    def remove_product(self, product, quantity=1):
        line = self.lines.get(product=product)
        if line.quantity - quantity != 0:
            line.quantity = line.quantity-quantity
            return line.save()
        else:
            return line.delete()

    def freeze(self):
        self.status = self.FROZEN
        self.save()

    def _get_total(self):
        """Посчитать сумму всех линий корзины"""
        #TODO посчитать всю сумму продуктов
        price = []
        for line in self.all_lines():
            price.append(line.get_price())
        return sum((int(price[i]) for i in range(0, len(price))))

    def submit(self):
        self.status = self.SUBMITTED
        self.date_created_submitted = now()
        return self.save()


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='lines')
    slug = models.SlugField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_lines')
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True)

    # class Meta:
    #     ordering = ['data_created', 'pk']

    def get_price(self):
       return self.product.invoice.price()

    def __str__(self):
        return f"продукт - {self.product.name} Kорзина - {self.basket}"