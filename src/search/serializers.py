from rest_framework import serializers
from src.catalogue.models import Attribute, ProductAttributeValue


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ('value_text', 'value_bool', 'value_integer', 'value_float', 'value_date',)


class AttributeFilterSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = ('name', 'type', 'values')

    def get_values(self, instance):
        values = instance.get_values()
        serialize = ProductAttributeValueSerializer(values, many=True)
        return serialize.data
