from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from src.basket.models import Basket
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


class BasketListApiView(ListAPIView):
    serializer_class = BasketSerializer

    def list(self, request):
        response = Response()
        try:
            cookie = request.COOKIES['basket']
            basket = Basket.objects.get(id=cookie)
            serializer = self.serializer_class(basket)
            response.data = serializer.data
            response.status_code = status.HTTP_200_OK
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.data = 'Корзина не найдена'
        return response


class BasketLineApiView(CreateAPIView):
    serializer_class = BasketLineSerializer
    #TODO добавить кол-во товара в корзину. Если товар уже добавлен, то увеличить кол-во
    #TODO высчитать стоимость товара по кол-ву добавленного товара
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        response = Response()
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = 1
            if 'quantity' in serializer.validated_data:
                quantity = serializer.validated_data['quantity']
            if 'basket' in request.COOKIES:
                try:
                    basket = Basket.objects.get(id=request.COOKIES['basket'])
                except:
                    raise serializers.ValidationError('Корзина не найдена')
            else:
                basket = Basket.objects.create()
            if basket.get_stock_info(product) > 0:
                basket.add_product(product, quantity)
            else:
                raise serializers.ValidationError(f"продукта {product} нет на складе")
            if request.user.is_active:
                basket.owner = request.user
            response.status_code = status.HTTP_201_CREATED
            response.data = 'Продукт добавлен в корзину'
            response.set_cookie(
                key='basket',
                value=basket.id,
                httponly=False,
            )
            return response
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class RemoveLineFromBasketView(DestroyAPIView):
    #TODO убрать продукт из корзины
    serializer_class = BasketLineSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            cookie = self.request.COOKIES['basket']
            basket = Basket.objects.get(id=cookie)
            product = Product.objects.get(id=pk)
            basket.remove_product(product)
        except:
            raise serializers.ValidationError('Линия уже удалена')


