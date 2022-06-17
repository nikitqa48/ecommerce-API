from django.db import models
from src.catalogue.models import Product


class Deals(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discount')
    discount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_end = models.DateTimeField()

    def __str__(self):
        return f"скидка {self.discount}% для {self.product.name}"


