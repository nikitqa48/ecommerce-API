from rest_framework import serializers
from .models import Product, Attribute, ProductClass, Catalogue, Category, CatalogCategory, ProductAttributeValue, ProductImage


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('name', 'type',)


class ImageForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'original', 'display_order')


class ProductClassSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=True)

    class Meta:
        model = ProductClass
        fields = ('attribute','name')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = ProductAttributeValue
        fields = ('value_text', 'value_bool', 'value_integer', 'value_float', 'value_date', 'attribute')


class RecomendedProductSerializer(serializers.ModelSerializer):
    images = ImageForProductSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('images', 'rating', 'name')


class ProductSerializer(serializers.ModelSerializer):
    product_class = ProductClassSerializer(read_only=True)
    index = serializers.IntegerField(required=False)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    in_stock = serializers.SerializerMethodField(read_only=True)
    images = ImageForProductSerializer(read_only=True, many=True)
    recommended_products = RecomendedProductSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('id','index','name', 'slug', 'date_created', 'date_updated','images', 'recommended_products',
                  'description', 'meta_title', 'meta_description', 'rating', 'product_class', 'attribute_values', 'in_stock')

    def get_in_stock(self, instance):
        return instance.in_stock()


class CategorySerializer(serializers.ModelSerializer):
    #TODO Посчитать кол-во продуктов в каждой категории и сложить в родительской
    children = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'id' ,'slug', 'children', 'product_count')

    def get_children(self, instance):
        children = Category.objects.filter(parent=instance)
        serializer = CategorySerializer(children, many=True)
        return serializer.data

    def get_product_count(self, instance):
        return instance.product_count()


class CatalogueSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, many=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Catalogue
        fields = ('name', 'parent', 'structure', 'category', 'children')

    def get_children(self, instance):
        children = Catalogue.objects.filter(parent=instance)
        serializer = CatalogueSerializer(children, many=True)
        return serializer.data