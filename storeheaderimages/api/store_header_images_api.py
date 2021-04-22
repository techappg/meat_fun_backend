from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.permissions import Is_admin
from product.models.store import Store
from storeheaderimages.models import Storeheader
from storeheaderimages.serializer.sroreheader_serializer import StoreHeaderImageSerializer, \
    StoreHeaderImageSerializerGet, StoreHeaderImageSerializerPatch


class StoreHeaderImages(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = StoreHeaderImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        store_id_string = serializer.validated_data.pop('store_id_list')
        store_id_list = store_id_string.split(",")

        data = serializer.validated_data
        stores = Store.objects.filter(storeId__in=store_id_list)

        if stores.exists():
            for store in stores:
                if data['default_image'] == True:
                    Storeheader.objects.filter(store=store).update(default_image=False)
                image = Storeheader.objects.create(store=store, **data)
        else:
            return Response("store dose not exists", status=status.HTTP_400_BAD_REQUEST)

        return Response("add successfully", status=status.HTTP_201_CREATED)


class StoreHeaderImagesGet(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = StoreHeaderImageSerializerGet

    def get(self, request, *args, **kwargs):
        store = self.kwargs['storeid']
        print(store)
        query = Storeheader.objects.filter(store__storeId=store)
        serializer = self.serializer_class(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreHeaderImagesDelete(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = StoreHeaderImageSerializerGet

    def delete(self, request, pk):
        try:
            queryset = Storeheader.objects.get(id=pk)
            queryset.delete()
            return Response("delete successfully", status=status.HTTP_200_OK)
        except:
            return Response("dose not exists", status=status.HTTP_400_BAD_REQUEST)


class StoreHeaderImagesRead(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = StoreHeaderImageSerializerGet

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            query = Storeheader.objects.get(pk=pk)
        except:
            return Response("id dose not exists", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(query, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreHeaderImagesPatch(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = StoreHeaderImageSerializerPatch

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            query = Storeheader.objects.get(pk=pk)
        except:
            return Response("id dose not exists", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(query, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            if serializer.validated_data.get('default_image') == True:
                try:
                    store = serializer.validated_data.pop('pos_store_id')
                    Storeheader.objects.filter(store__storeId=store).update(default_image=False)
                except:
                    pass

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreHeaderImagesRandem(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = StoreHeaderImageSerializerGet

    def get(self, request, *args, **kwargs):
        store = Store.objects.filter(is_enable=True).first()
        query = Storeheader.objects.filter(store=store)
        serializer = self.serializer_class(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)