from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', CatatalogListView.as_view()),
    path('<slug:slug>/list/', ProductsListForCategoryView.as_view()),
    path('<slug:slug>/detail/', ProductDetailView.as_view())
]