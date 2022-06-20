from django.db import models
from src.catalogue.models import Product
from src.shipment.models import Shipment
from src.payment.models import Payment


class Customer(models.Model):
    address = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    email = models.EmailField()
    phone = models.IntegerField()


class OrderDetail(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Order(models.Model):
    totalprice = models.FloatField(editable=False)
    STATUS_CHOICE = (
        ('0', 'Заказ принят'),
        ("1", "В процессе"),
        ("2", "Завершен")
    )
    orderstatus = models.CharField(max_length=500, choices=STATUS_CHOICE)
    detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()