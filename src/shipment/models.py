from django.db import models


class Shipment(models.Model):
    address = models.CharField(max_length=500)
    method = models.CharField(max_length=500)

