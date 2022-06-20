from django.db import models
from pytils.translit import slugify
from django.core.exceptions import ImproperlyConfigured, ValidationError
from datetime import date, datetime
from src.customAuth.models import CustomUser as User
from django.db.models import Avg
from io import BytesIO
from PIL import Image
from django.core.files import File


def create_slug(title, new_slug=None):
    slug = slugify(title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(title, new_slug=new_slug)
    return slug


def compress(image):
    im = Image.open(image).convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=80)
    new_image = File(im_io, name=image.name)
    return new_image


class Category(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
    STRUCTURE_CHOICES = (
        (STANDALONE, 'Самостоятельная категория'),
        (PARENT, 'Родительская категория'),
        (CHILD, 'Дочерняя категория')
    )
    structure = models.CharField("category structure", max_length=10, choices=STRUCTURE_CHOICES,
                                 default=STANDALONE)
    meta_descriptions = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    _slug_separator = '/'

    def __str__(self):
        if self.structure == self.CHILD:
            return f" Категория {self.name} для категории {self.parent.name} "
        return self.name

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        if self.parent:
            self.structure = self.CHILD
            self.parent.structure = self.PARENT
            self.parent.save()
        return super(Category, self).save(*args, **kwargs)

    def product_count(self):
        count = Product.objects.filter(categories__id=self.id).count()
        return count


class Attribute(models.Model):
    """Атрибут для группы атрибутов. Например Характеристики экрана:матрица"""
    name = models.CharField(max_length=255)
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    DATETIME = "datetime"
    OPTION = "option"
    MULTI_OPTION = "multi_option"
    ENTITY = "entity"
    FILE = "file"
    IMAGE = "image"
    TYPE_CHOICES = (
        (TEXT, "Text"),
        (INTEGER, "Integer"),
        (BOOLEAN, "True / False"),
        (FLOAT, "Float"),
        (RICHTEXT, "Rich Text"),
        (DATE, "Date"),
        (DATETIME, "Datetime"),
        (OPTION, "Option"),
        (MULTI_OPTION, "Multi Option"),
        (ENTITY, "Entity"),
        (FILE, "File"),
        (IMAGE, "Image"),
    )
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], max_length=20, verbose_name="Type")
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_attributes', blank=True)
    # option_group = models.ForeignKey(AttributeOptionGroup,
    #                                  on_delete=models.CASCADE,
    #                                  null=True, blank=True,
    #                                  related_name='product_attributes')

    def __str__(self):
        return self.name

    def get_values(self):
        values = ProductAttributeValue.objects.filter(attribute=self)
        return values

    def save_value(self, product, value):
        try:
            value_obj = product.attribute_values.get(attribute=self)
        except ProductAttributeValue.DoesNotExist:
            if value is None or value == '':
                return
                value_obj = object.create(product=product, attribute=self)

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type)
        validator(value)

    def _validate_text(self, value):
        if not isinstance(value, str):
            raise ValidationError("Must be str")

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError('Must be float')

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError("Must be an integer")

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError("Must be a date or datetime")

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError("Must be a boolean")


class ProductClass(models.Model):
    """Класс продукта, например - футболка или цвет айфона"""

    name = models.CharField(max_length=5000)
    required_shipping = models.BooleanField(default=True)
    track_stock = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        return super(Brand, self).save(*args, **kwargs)


class Catalogue(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
    STRUCTURE_CHOICES = (
        (STANDALONE, 'Самостоятельная'),
        (PARENT, 'Родительская'),
        (CHILD, 'Дочерняя')
    )
    structure = models.CharField("Структура каталога", max_length=10, choices=STRUCTURE_CHOICES,
                                 default=STANDALONE)
    category = models.ManyToManyField(Category, through="CatalogCategory")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        return super(Catalogue, self).save(*args, **kwargs)


class CatalogCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)



class Discount(models.Model):
    percent = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_end = models.DateTimeField()

    # def __str__(self):
    #     return f"скидка {self.discount}% для {self.product.name}"


class Product(models.Model):
    name = models.CharField(max_length=5000)
    slug = models.SlugField(blank=True)
    STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
    STRUCTURE_CHOICES = (
        (STANDALONE, 'Stand-alone product'),
        (PARENT, 'Parent product'),
        (CHILD, 'Child product')
    )
    structure = models.CharField("Product structure", max_length=10, choices=STRUCTURE_CHOICES, default=STANDALONE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True)
    is_public = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name="Parent product",
        help_text="Выбирайте родительский продукт, только если вы создаете дочерний товар. Например, если это размер 4 определенного типа футболки. Оставьте пустым,"
                  "если это автономный продукт (т.е. существует только одна версия этого продукта)")
    meta_title = models.TextField(blank=True, null=True)
    _price = models.IntegerField(null=True, blank=True)
    meta_description = models.TextField(blank=True, null=True)
    product_class = models.ForeignKey(ProductClass,null=True, blank=True,
                                      on_delete=models.PROTECT, related_name="products",
                                      help_text='Выберите тип продукта')
    rating = models.FloatField(null=True, editable=False)
    attributes = models.ManyToManyField(
        Attribute,
        through='ProductAttributeValue',
        verbose_name="Характеристики",
        help_text="Атрибут продукта — это то, что этот продукт может иметь, например, размер, указанный его классом")
    categories = models.ManyToManyField(Category, through='ProductCategory')
    recommended_products = models.ManyToManyField(
        'self', through='ProductRecommendation', blank=True,
        verbose_name="Recommended products",
        help_text="Рекомендации для продукта")
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        return super(Product, self).save(*args, **kwargs)

    def update_rating(self):
        """
        Recalculate rating field
        """
        self.rating = self.calculate_rating()
        self.save()

    def calculate_rating(self):
        reviews = Review.objects.filter(product=self)
        rating = None
        if reviews.count() > 0:
            average = reviews.aggregate(Avg("rating"))["rating__avg"]
            rating = float(average)
        return rating

    def has_review_by(self, user):
        if user.is_anonymous:
            return False
        return Review.objects.filter(user=user).exists()

    def is_review_permitted(self, user):
        if user.is_authenticated:
            return not self.has_review_by(user)
        else:
            return False

    @property
    def is_standalone(self):
        return self.structure == self.STANDALONE

    @property
    def is_parent(self):
        return self.structure == self.PARENT

    @property
    def is_child(self):
        return self.structure == self.CHILD

    def in_stock(self):
        stock = Stock.objects.filter(product=self)
        return stock.exists()

    class Meta:
        ordering = ['date_created']


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField('кол-во запасов')
    updated = models.DateTimeField(auto_now=True)


class ProductCategory(models.Model):
    """Категория продукта, например - стиральная машина. Родительская категория - бытовая техника. Промежуточная модель"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='category')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Категория продукта для {self.product}"


class ProductAttributeValue(models.Model):
    """Промежуточная модель между группой атрибутов и атрибутом"""

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    """Атрибут, связь один ко многим. Например: высота """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    value_text = models.TextField(blank=True, null=True, db_index=True)
    value_bool = models.BooleanField(blank=True, null=True, db_index=True)
    value_integer = models.IntegerField(blank=True, null=True, db_index=True)
    value_float = models.FloatField(blank=True, null=True, db_index=True)
    value_date = models.DateField(blank=True, null=True, db_index=True)
    value_datatime = models.DateTimeField(blank=True, null=True, db_index=True)
    # group = models.ForeignKey(AttributeGroup)
    #TODO создать группу для атрибутов

    class Meta:
        unique_together = ('attribute', 'product')

    def __str__(self):
        value = getattr(self, f"value_{self.attribute.type}")
        return f"{self.attribute.type}, {value}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    """Продукт, к которому привязано изображение (один ко многим) """
    original = models.ImageField(upload_to='images')
    """Само изображение"""
    display_order = models.PositiveIntegerField(default=0)
    """Номер по которому отображается фото"""
    data_created = models.DateTimeField(auto_now_add=True)
    """дата создания фото"""

    def __str__(self):
        return f"Изображение для {self.product}"

    def is_primary(self):
        '''Возвращает bool, если изображение основное'''
        return self.display_order == 0

    def save(self, *args, **kwargs):
        new_image = compress(self.original)
        self.original = new_image
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['display_order',]


class ProductRecommendation(models.Model):
    """
    'Through' model for product recommendations
    """
    primary = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='primary_recommendations',
        verbose_name="Primary product")
    recommendation = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Recommended product")
    ranking = models.PositiveSmallIntegerField(
        'Ranking', default=0, db_index=True,)

    class Meta:
        app_label = 'catalogue'
        ordering = ['primary', '-ranking']
        unique_together = ('primary', 'recommendation')
        verbose_name = 'Product recommendation'
        verbose_name_plural = 'Product recomendations'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


