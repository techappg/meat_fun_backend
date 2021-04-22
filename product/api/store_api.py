from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS, BasePermission
from rest_framework.response import Response

from backend_roc.utils.permissions import Is_admin
from product.models.order import Order
from product.models.products import Product
from product.models.store import Store
from product.serializer.store_serializer import store_Serializer
from product.utils.encryption_decryption import encrypt, decrypt


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class get_store_View(viewsets.ModelViewSet):
    permission_classes = [Is_admin, ]
    serializer_class = store_Serializer
    queryset = Store.objects.all()

    def create(self, request,  *args, **kwargs):
        serializer = store_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            MERCHANT_KEY = encrypt(serializer.validated_data.get('MERCHANT_KEY'))
            MID = encrypt(serializer.validated_data.get('MID'))

            data = serializer.validated_data
            data['MERCHANT_KEY'] = MERCHANT_KEY
            data['MID'] = MID

            serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        store = self.queryset.get(id=self.kwargs['pk'])
        serializer = self.get_serializer(store, data=request.data, context={'request': request})
        if serializer.is_valid():
            MERCHANT_KEY = encrypt(serializer.validated_data.get('MERCHANT_KEY'))
            MID = encrypt(serializer.validated_data.get('MID'))

            data = serializer.validated_data
            data['MERCHANT_KEY'] = MERCHANT_KEY
            data['MID'] = MID
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        category = self.queryset.get(id=self.kwargs['pk'])
        serializer = self.serializer_class(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            data = serializer.validated_data
            if serializer.validated_data.get('MERCHANT_KEY'):
                MERCHANT_KEY = encrypt(serializer.validated_data.get('MERCHANT_KEY'))
                data['MERCHANT_KEY'] = MERCHANT_KEY
                print(decrypt(serializer.validated_data.get('MERCHANT_KEY')))

            if serializer.validated_data.get('MID'):
                MID = encrypt(serializer.validated_data.get('MID'))
                data['MID'] = MID
                print(decrypt(serializer.validated_data.get('MID')))
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request,  *args, **kwargs):
        try:
            id = self.kwargs['pk']
            store = Store.objects.get(id=id)
            order = Order.objects.filter(items__item__store=store)
            print(order)
            if order.exists():
                return Response("store have order history please do not delete store use enable disable ", status=status.HTTP_400_BAD_REQUEST)
            store.delete()
            return Response("delete successfully ", status=status.HTTP_200_OK)
        except:
            return Response("id dose not exists please check your id ", status=status.HTTP_400_BAD_REQUEST)