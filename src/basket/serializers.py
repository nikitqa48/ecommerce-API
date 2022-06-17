from rest_framework import serializers
from .models import *
from src.catalogue.serializers import ProductSerializer


class BasketLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    stock = serializers.SerializerMethodField()
    basket_id = serializers.IntegerField(required=False)

    class Meta:
        model = BasketLine
        fields = ('id', 'slug', 'product', 'quantity', 'stock', 'basket_id')

    def get_stock(self, instance):
        quantity = instance.basket.get_stock_info(instance.product)
        return quantity

    def validate_product(self,data):
        product = Product.objects.filter(id=data['index'])
        if not product.exists():
            raise serializers.ValidationError("Продукт не найден")
        return product.first()

    def validate_basket(self,data):
        basket = Basket.objects.filter(id=data)
        if not basket.exists():
            raise serializers.ValidationError(f"Корзины с id {data} не существует")
        return basket.first()


class BasketSerializer(serializers.ModelSerializer):
    lines = BasketLineSerializer(many=True, required=False)

    class Meta:
        model = Basket
        fields = ('lines',)

