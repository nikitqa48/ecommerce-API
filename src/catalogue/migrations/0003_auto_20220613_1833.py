# Generated by Django 3.2.13 on 2022-06-13 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceproduct',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='invoiceproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='Discount',
        ),
        migrations.DeleteModel(
            name='InvoiceProduct',
        ),
    ]
