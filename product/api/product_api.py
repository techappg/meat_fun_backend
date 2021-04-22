from django.db.models import Count
from rest_framework import exceptions

from backend_roc.utils.permissions import Is_admin
from product.models.order import Order
from product.models.products import Product, Images
from product.models.store import Store
from product.serializer.order_serializer import order_Serializer
from product.serializer.product_serializer import ProductSerializer, addProductSerializer, UpdateProductSerializer, \
    Images_Serializer, Update_store_products_Serializer, PosEnable
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser 
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView
)

from product.serializer.product_update_pos_serializer import PosProductSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subcategory", "category"]

    permission_classes = [AllowAny, ]

    def get_queryset(self):
        snippets = Product.objects.filter(Enable=True).order_by('-created_at')
        return snippets


class AdminProductListView(generics.ListAPIView):
    permission_classes = [Is_admin, ]
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
    permission_classes = [Is_admin, ]
    serializer_class = addProductSerializer
    queryset = Product.objects.all()


class UpdateproductView(UpdateAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = UpdateProductSerializer
    queryset = Product.objects.all()


class delete_productView(DestroyAPIView):
    permission_classes = [Is_admin, ]
    # queryset = Product.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            id = self.kwargs['pk']
            queryset = Product.objects.get(id=id)
            order = Order.objects.filter(items__item=queryset)
            if order.exists():
                return Response("product have order history please do not delete product use enable disable ", status=status.HTTP_400_BAD_REQUEST)
            queryset.delete()
            return Response("delete successfully ", status=status.HTTP_200_OK)
        except:
            return Response("id dose not exists please check your id ", status=status.HTTP_400_BAD_REQUEST)


class store_ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subcategory", "category", "store__id"]
    queryset = Product.objects.filter(Enable=True)

    # def filter_queryset(self, queryset):
    #     id = self.kwargs['pk']
    #     try:
    #         store = Store.objects.get(id=id)
    #     except Store.DoesNotExist:
    #         raise exceptions.NotFound(detail="Store dose not exists")
    #     queryset = Product.objects.filter(store=store)
    #     for backend in list(self.filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, self)
    #     return queryset


class store_product_updateView(UpdateAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Update_store_products_Serializer
    queryset = Product.objects.all()


class tranding_ListView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer

    def get(self, request):
        name = []
        # id = []
        product_list = []
        order = Order.objects.filter(order_status=True, items__item__Enable=True).values(
            'items__item__id',
            'items__item__name'
        ).annotate(count=Count('items__item__name')).order_by('-count')[:20]

        for od in order:
            if not od['items__item__name'] in name:
                name.append(od['items__item__name'])
                try:
                    queryset = Product.objects.get(id=od['items__item__id'])
                    product_list.append(queryset)
                except:
                    pass

        # if id is not None:
        #     for id in id:
        #         if id == None:
        #             pass
        #         else:
        #             queryset = Product.objects.get(id=id)
        #             product_list.append(queryset)

        serializer = ProductSerializer(product_list, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class PosProductProductView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PosProductSerializer

    def post(self, request):
        serializer = PosProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product_code = serializer.data.get('product_code')
            store_id = serializer.data.get('store_id')
            price = serializer.data.get('price')

            if product_code and store_id:
                query = Product.objects.filter(store__storeId=store_id, product_code=product_code)
                if query.exists():
                    pass
                else:
                    return Response("dose not exixts", status=status.HTTP_400_BAD_REQUEST)

                for product in query:
                    product.price = price
                    product.save()

                return Response("successfully update", status=status.HTTP_200_OK)
            if product_code:
                query = Product.objects.filter(product_code=product_code)
                if query.exists():
                    pass
                else:
                    return Response("product code dose not exixts", status=status.HTTP_400_BAD_REQUEST)

                for product in query:
                    product.price = price
                    product.save()
            return Response("successfully update", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PosEnableProductView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PosEnable

    def post(self, request, pk):
        serializer = PosEnable(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Enable = serializer.data.get("Enable_disenable")
            print(Enable)
            queryset = Product.objects.get(product_code=pk)
            queryset.Enable = Enable
            queryset.save()
            return Response("successfully update", status=status.HTTP_200_OK)
        except:
            return Response("id dose not exists", status=status.HTTP_400_BAD_REQUEST)


class TrandingStoreListView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        store_id = self.kwargs['store_id']
        # name = []
        # id = []
        # product_list = []
        # print(store_id)
        # order = Order.objects.filter(order_status=True, items__item__Enable=True, items__item__store__storeId=store_id).values(
        #     'items__item__id',
        #     'items__item__name'
        # ).annotate(count=Count('items__item__name')).order_by('-count')[:20]

        # for od in order:
        #     if not od['items__item__name'] in name:
        #         name.append(od['items__item__name'])
        #         try:
        #             queryset = Product.objects.get(id=od['items__item__id'])
        #             product_list.append(queryset)
        #         except:
        #             pass

        order = Product.objects.filter(
                                    cart__ordered=True,
                                    cart__item__Enable=True,
                                    cart__item__store__storeId=store_id
                                       ).annotate(count=Count('cart__item__name')).order_by('-count')[:20]
        serializer = ProductSerializer(order, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)