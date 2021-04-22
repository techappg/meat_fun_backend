from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Count

from product.models.order import Order
from product.models.products import Product
from product.models.store import Store
from product.serializer.product_serializer import ProductSerializer
from datetime import datetime


class DemoProducts(GenericAPIView):
    permission_classes = [AllowAny, ]

    def get(self, request, ):
        store = Store.objects.filter(is_enable=True).first()
        queryset = Product.objects.filter(store=store)
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DemoTrendingProducts(GenericAPIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        store = Store.objects.filter(is_enable=True).first()
        print(store)
        queryset = Product.objects.filter(
            cart__ordered=True,
            cart__item__Enable=True,
            cart__item__store=store
        ).annotate(count=Count('cart__item__name')).order_by('-count')[:20]
        print(queryset)
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class Time(GenericAPIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        data = dict()
        data['time'] = current_time
        return Response(data, status=status.HTTP_200_OK)


class DemoProductFilter(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subcategory", "category"]

    def filter_queryset(self, queryset):
        # id = self.kwargs['pk']
        try:
            store = Store.objects.filter(is_enable=True).first()
        except Store.DoesNotExist:
            raise exceptions.NotFound(detail="Store dose not exists")
        queryset = Product.objects.filter(store=store)
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset