from product.models.cart import Cart
from product.models.products import Product
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView
)
from product.serializer.cart_serializer import CartViewSerializer, Cart_update_Serializer, Cart_create_Serializer


class AddToCartView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = Cart_create_Serializer

    def post(self, request):
        serializer = Cart_create_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            item = serializer.data.get("item")
            quantity = serializer.data.get("quantity")
            store_id = serializer.data.get('store_id')
            # print(item)
            # item = get_object_or_404(Product, id=id)
            user = self.request.user
            cart_qs = Cart.objects.filter(item__id=item, user=user, ordered=False, store_id=store_id)
            if cart_qs.exists():
                cart = cart_qs[0]
                cart.quantity += 1
                cart.save()
                return Response("Product Successfully Add", status.HTTP_201_CREATED)
            else:
                item_obj = get_object_or_404(Product, id=item)
                Cart.objects.create(item=item_obj, user=user, quantity=quantity, ordered=False, store_id=store_id)
                return Response("Product Successfully Add", status.HTTP_201_CREATED)


class cartView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, store_id=None):
        store_id = self.kwargs['store_id']
        user = self.request.user
        snippets = Cart.objects.filter(user=user, ordered=False, store_id=store_id)
        serializer = CartViewSerializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)


class delete_cartView(DestroyAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Cart.objects.all()


class cart_update_View(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = Cart_update_Serializer
    queryset = Cart.objects.all()
