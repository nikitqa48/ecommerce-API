from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from src.catalogue.models import Attribute, Category, Product
from .serializers import AttributeFilterSerializer
from src.catalogue.serializers import ProductSerializer
import django_filters
from rest_framework import filters


class AttributeForProductCategory(ListAPIView):
    serializer_class = AttributeFilterSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        if category.structure == 'child':
            category = category.parent
        attributes = Attribute.objects.filter(categories=category)
        return attributes


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    search_fields = ['name', ]
    filter_backends = [filters.SearchFilter]
