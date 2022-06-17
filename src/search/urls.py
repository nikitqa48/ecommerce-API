from django.urls import path, include
from .views import *

urlpatterns = [
    path('<slug:slug>/filters/', AttributeForProductCategory.as_view()),
    path('products/', ProductListAPIView.as_view())
]