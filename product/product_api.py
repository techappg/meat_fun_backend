from rest_framework.views import APIView

from product.models.order import Order
from product.models.products import Product, Images
from product.models.store import Store
from product.serializer.order_serializer import order_Serializer
from product.serializer.product_serializer import ProductSerializer, addProductSerializer, UpdateProductSerializer, \
    Images_Serializer, Update_store_products_Serializer
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser 
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subcategory", "category"]

    permission_classes = [AllowAny, ]

    def get_queryset(self):
        snippets = Product.objects.filter(Enable=True).order_by('-created_at')
        return snippets

class AdminProductListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category", "subcategory"]
    # search_fields = ['name', 'subcategory', 'category']
    queryset = Product.objects.all().order_by('-created_at')


class productDetailView(RetrieveAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class addproductView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = addProductSerializer
    queryset = Product.objects.all()

class UpdateproductView(UpdateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UpdateProductSerializer
    queryset = Product.objects.all()

class delete_productView(DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()

class store_ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subcategory', 'category']

    def filter_queryset(self, queryset):
        id = self.kwargs['pk']
        store = Store.objects.get(id=id)
        queryset = Product.objects.filter(store=store)
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

class store_product_updateView(UpdateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Update_store_products_Serializer
    queryset = Product.objects.all()

class tranding_ListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    # queryset = Order.objects.all()
    def get_queryset(self):
        order = Order.objects.filter(order_status=True)
        b = order[0]
        for ord in b.items.filter():
            # print(ord.item.id)
            queryset = Product.objects.filter(id=ord.item.id)
        return queryset
