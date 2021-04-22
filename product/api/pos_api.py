import json

import requests
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.const import POS_TEX_GET, POS_CAT_GET, POS_CREATE
from backend_roc.utils.permissions import Is_admin
from product.models.Subcategory import Subcategory
from product.models.category import Category
from product.models.products import Product
from product.models.store import Store
from product.serializer.pos_serializer import PosProductPostSerializer


class PosTaxGet(GenericAPIView):
    permission_classes = [Is_admin, ]

    def get(self, request):
        response = requests.get(POS_TEX_GET).json()
        return Response(response, status=status.HTTP_200_OK)


class PosCatGet(GenericAPIView):
    permission_classes = [Is_admin, ]

    def get(self, request):
        response = requests.get(POS_CAT_GET).json()
        return Response(response, status=status.HTTP_200_OK)


class PosProductPost(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PosProductPostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            category = Category.objects.get(id=serializer.data.get('category'))
        except:
            return Response("category id dose not exists", status=status.HTTP_400_BAD_REQUEST)

        store_list = serializer.data.get('store')
        if store_list:
            store_id_list = store_list.split(",")
            stores = Store.objects.filter(storeId__in=store_id_list)
        else:
            return Response("Store id dose not exists", status=status.HTTP_400_BAD_REQUEST)

        ItemName = serializer.data.get('ItemName')
        ItemType = serializer.data.get('ItemType')
        ItemCategory = serializer.data.get('ItemCategory')
        itemPrice = serializer.data.get('itemPrice')
        taxid = serializer.data.get('taxid')

        if stores.exists():
            for store in stores:
                data = {"ItemName": ItemName, "ItemType": ItemType, "ItemCategory": int(ItemCategory), "itemPrice": int(itemPrice),
                        "Items":[{"OutletId": int(store.storeId), "taxid": int(taxid)}]
                        }

                pos_api = requests.post(POS_CREATE, json=data)
                if pos_api.status_code != 200:
                    return Response({"error": json.loads(pos_api.text)}, status.HTTP_400_BAD_REQUEST)

                pos_item_id = pos_api.json()

                product = Product.objects.create(
                    category=category,
                    store=store,
                    name=serializer.data.get('name'),
                    description=serializer.data.get('description'),
                    price=serializer.data.get('price'),
                    quantity_type=serializer.data.get('quantity_type'),
                    productUsage=serializer.data.get('productUsage'),
                    keyword=serializer.data.get('keyword'),
                    product_code=pos_item_id['id'],
                    default_image=request.data.get('default_image'),
                    Enable=serializer.data.get('Enable'),
                    quantity=serializer.data.get('quantity'),
                    seo_title=serializer.data.get('seo_title'),
                )
                try:
                    subcategory = Subcategory.objects.get(id=serializer.data.get('subcategory'))
                    product.subcategory = subcategory
                    product.save()
                except:
                   pass
        else:
            return Response("Store id dose not exists", status=status.HTTP_400_BAD_REQUEST)
        return Response("add successfully", status=status.HTTP_200_OK)

