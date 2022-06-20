from django.db import models

class Payment(models.Model):
    # methods = models.ForeignKey()
    date = models.DateTimeField()
    card_number = models.IntegerField()
    card_holder = models.CharField(max_length=500)
    cvc = models.IntegerField()
