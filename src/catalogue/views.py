from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .models import *
from .serializers import CatalogueSerializer, ProductSerializer


class CatatalogListView(ListAPIView):
    queryset = Catalogue.objects.filter(structure='parent')
    serializer_class = CatalogueSerializer


class ProductsListForCategoryView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        queryset = Product.objects.filter(categories__slug=slug)
        return queryset


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()