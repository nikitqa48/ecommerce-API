from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', BasketListApiView.as_view()),
    path('add_product/', BasketLineApiView.as_view()),
    path('remove/<int:pk>', RemoveLineFromBasketView.as_view())
]