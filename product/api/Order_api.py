import json
import requests
from backend_roc.utils.const import POS_MACHINE_API
from product.models.address import Address
from product.models.cart import Cart
from product.models.coupon import Coupon
from product.models.order import Order, Transaction
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView
)

import razorpay
from datetime import date
from product.models.store import Store
from product.serializer.order_serializer import order_Serializer, Transaction_Serializer, update_order_Serializer, \
    post_order_Serializer, id_store_id

#client = razorpay.Client(auth=("rzp_live_CbMRTtLiIOtCU6", "Uuv9j1vj3ccZHCbGMeIKJeBQ"))

client = razorpay.Client(auth=("rzp_test_UxeO6rtAvoDjr0", "VTJklwITkvijiiQTYIw9sqSm"))


class Order_View(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = post_order_Serializer

    def get(self, request, format=None):
        snippets = Order.objects.filter(order_status=True)
        serializer = order_Serializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = post_order_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile = serializer.data.get('mobile')
            time = serializer.data.get('time')
            Choice = serializer.data.get('Choice')
            payment_mode = serializer.data.get('payment_mode')
            coupon = serializer.data.get('coupon')
            store_id = serializer.data.get('store_id')

            user = self.request.user
            cart = Cart.objects.filter(user=user, ordered=False, store_id=store_id)
            order_qs = Order.objects.filter(user=user, order_status=False)
            if cart.exists():
                if order_qs.exists():
                    pass
                else:
                    order = Order.objects.create(user=user, order_status=False, store_id=store_id,)
                    items = order.items
                    for item in cart:
                        items.add(item)
                    order.save()

                # if coupon:
                #     try:
                #         code = Coupon.objects.get(coupon_code=coupon)
                #         order_qs.update(coupon=code)
                #     except:
                #         return Response("coupon dose not exists", status.HTTP_400_BAD_REQUEST)

                real_amount = float(order_qs[0].get_total())
                amount = float(order_qs[0].get_total()) * 100
                # amount = 1000

                print("amount", amount)
                order_currency = 'INR'
                order_receipt = 'order_rcptid_11'

                order_id = client.order.create(dict(amount=amount,
                                                    currency=order_currency,
                                                    receipt=order_receipt
                                                    ))
                if order_id['status'] != 'created':
                    return Response(" order failed try again", status.HTTP_400_BAD_REQUEST)

                if payment_mode == "COD" and Choice == 'Picking':
                    order_qs.update(order_id=order_id['id'],
                                    delivery_time=time,
                                    mobile_num=mobile,
                                    amount=real_amount,
                                    choice=Choice,
                                    payment_mode=payment_mode,
                                    store_id=store_id,
                                    )
                    print("Picking")

                if payment_mode == "COD" and Choice == 'Home Delivery':
                    try:
                        shipping_address = Address.objects.get(user=user, address_type="Shipping")
                    except:
                        return Response("Address Dose not exists", status=status.HTTP_400_BAD_REQUEST)
                    order_qs.update(order_id=order_id['id'],
                                    shipping_address=shipping_address,
                                    delivery_time=time,
                                    mobile_num=mobile,
                                    amount=real_amount,
                                    choice=Choice,
                                    payment_mode=payment_mode,
                                    store_id=store_id,
                                    )
                    print("home")
                if payment_mode == "COD":
                    responce_data = dict()
                    for qs in order_qs:
                        # print(self.request.user.first_name)
                        responce_data['OrderNo'] = qs.id
                        responce_data['fk_TableId_num'] = 1
                        responce_data['Outletid_num'] = qs.store_id
                        responce_data['NoOfGuest'] = 1
                        responce_data['customerMobile'] = qs.mobile_num
                        responce_data['cityCode'] = 5
                        responce_data['DiscountCode'] = 0
                        responce_data['CustomerName'] = self.request.user.first_name
                        if qs.shipping_address:
                            responce_data['CustomerAddress'] = qs.address()
                        else:
                            responce_data['CustomerAddress'] = ""
                        responce_data['DiscountAmount'] = 0
                        responce_data['TotalAmount'] = float(real_amount)
                        if qs.payment_mode == 'COD':
                            responce_data['PayMode'] = 1
                            responce_data['TotalAmountPaid'] = 0
                        else:
                            responce_data['PayMode'] = 7
                            responce_data['TotalAmountPaid'] = float(real_amount)
                        responce_data['Items'] = []

                        for c in cart:
                            data = {
                                "fk_ItemId_num": int(c.item.product_code),
                                "Qty_num": c.quantity,
                                "Price_num": float(c.get_final_amount()),
                            }
                            responce_data['Items'].append(data)
                    print(responce_data)
                    url = POS_MACHINE_API
                    send = requests.post(url, data=json.dumps(responce_data), headers={'Content-Type': 'application/json'})
                    print(send)
                    if send.status_code != 201:
                        return Response({
                            "error": json.loads(send.text)
                        }, status.HTTP_400_BAD_REQUEST)
                    print(send.content)
                    cart.update(ordered=True)
                    order_qs.update(order_status=True)
                if payment_mode == "ONLINE PAY" and Choice == 'Home Delivery':
                    try:
                        shipping_address = Address.objects.get(user=user, address_type="Shipping")
                    except:
                        return Response("Address Dose not exists", status=status.HTTP_400_BAD_REQUEST)
                    order_qs.update(order_id=order_id['id'],
                                    shipping_address=shipping_address,
                                    delivery_time=time,
                                    mobile_num=mobile,
                                    amount=real_amount,
                                    choice=Choice,
                                    payment_mode=payment_mode,
                                    store_id=store_id,
                                    )
                    print("ONLINE PAY")

                else:
                    order_qs.update(order_id=order_id['id'],
                                    amount=real_amount,
                                    delivery_time=time,
                                    mobile_num=mobile,
                                    choice=Choice,
                                    )

                final_response = dict()
                final_response['error'] = False
                data = {
                    "order_id": order_id['id'],
                    "amount": real_amount,
                }
                final_response['data'] = data
                return Response(final_response, status.HTTP_200_OK)
            else:
                final_response = dict()
                final_response['error'] = True
                data = {
                    "MSG": "Empty cart"
                }
                final_response['data'] = data
                return Response(final_response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Transaction_views(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Transaction_Serializer

    def post(self, request, format=None):
        serializer = Transaction_Serializer(data=request.data)
        # try:
        if serializer.is_valid():
            serializer.save()
            order_id = serializer.data.get('razorpay_order_id')
            clint_signature = client.utility.verify_payment_signature(serializer.data)
            if clint_signature is None:
                order_qs = Order.objects.get(order_id=order_id)
                # order_qs.order_status = True
                # order_qs.save()
                cart = Cart.objects.filter(user=self.request.user, ordered=False)
                responce_data = dict()
                responce_data['OrderNo'] = order_qs.id
                responce_data['fk_TableId_num'] = 1
                responce_data['Outletid_num'] = order_qs.store_id
                responce_data['NoOfGuest'] = 1
                responce_data['customerMobile'] = order_qs.mobile_num
                responce_data['cityCode'] = 5
                responce_data['DiscountCode'] = 0
                responce_data['CustomerName'] = self.request.user.first_name
                if order_qs.shipping_address:
                    responce_data['CustomerAddress'] = order_qs.address()
                else:
                    responce_data['CustomerAddress'] = ""
                responce_data['DiscountAmount'] = 0
                responce_data['TotalAmount'] = float(order_qs.amount)
                if order_qs.payment_mode == 'COD':
                    responce_data['PayMode'] = 1
                    responce_data['TotalAmountPaid'] = 0
                else:
                    responce_data['PayMode'] = 7
                    responce_data['TotalAmountPaid'] = float(order_qs.amount)
                responce_data['Items'] = []
                for c in cart:
                    data = {
                        "fk_ItemId_num": int(c.item.product_code),
                        "Qty_num": c.quantity,
                        "Price_num": float(c.get_final_amount()),
                    }
                    responce_data['Items'].append(data)
                print(responce_data)
                url = POS_MACHINE_API
                send = requests.post(url, data=json.dumps(responce_data), headers={'Content-Type': 'application/json'})
                print('data', send)
                if send.status_code != 201:
                    return Response({
                        "error": send.text
                    }, status.HTTP_400_BAD_REQUEST)
                cart.update(ordered=True)
                order_qs.order_status = True
                order_qs.save()
                return Response(" order successful ", status.HTTP_200_OK)
            else:
                return Response("Order failed", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response("Oops something went wrong", status.HTTP_400_BAD_REQUEST)



class Update_status_View(UpdateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = update_order_Serializer
    queryset = Order.objects.all()


class user_order_views(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = order_Serializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user, order_status=True).order_by('-created_at')
        return queryset


class get_order_id_ListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = order_Serializer

    def get_queryset(self):
        id = self.kwargs['pk']
        queryset = Order.objects.filter(id=id, user=self.request.user, order_status=True).order_by('-created_at')
        return queryset


class store_order_list_views(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = id_store_id

    def post(self, request):
        serializer = id_store_id(data=request.data)

        if serializer.is_valid(raise_exception=True):
            store_id = serializer.data.get('id')
            start_date = serializer.data.get('start_date')
            end_date = serializer.data.get('end_date')
            try:
                if store_id:
                    sstoreid = store_id.split(",")
                    store_list = Store.objects.filter(id__in=sstoreid).values_list("store_name", flat=True)
                    final_response = dict()
                    final_response['data'] = []

                    for store in store_list:
                        queryset = Order.objects.filter(
                                                        created_at__range=[start_date, end_date],
                                                        items__item__store__store_name=store,
                                                        order_status=True, ).values(
                            'items__item__store__store_name',
                            'order_id',
                            'amount',
                            'choice',
                            'payment_mode',
                            'created_at',
                        ).order_by('-created_at')
                        if queryset.exists():
                            # final_response['store_name'] = store
                            for q in queryset:
                                data = {
                                    "store_name": q['items__item__store__store_name'],
                                    "order_id": q['order_id'],
                                    "amount": q['amount'],
                                    "choice": q['choice'],
                                    "payment_mode": q['payment_mode'],
                                    "created_at": q['created_at'],
                                }
                                final_response['data'].append(data)
                            # qss.append(data)

                    return Response(final_response, status.HTTP_200_OK)
                else:
                    store = Store.objects.all()
                    id = []
                    for qsq in store:
                        a = qsq.store_name
                        id.append(a)
                    final_response = dict()
                    final_response['data'] = []

                    for y in id:

                        queryset = Order.objects.filter(items__item__store__store_name=y,
                                                        created_at__range=[start_date, end_date],
                                                        order_status=True,).values(
                            'items__item__store__store_name',
                            'order_id',
                            'amount',
                            'choice',
                            'payment_mode',
                            'created_at',
                        ).order_by('-created_at')
                        if queryset.exists():

                            # final_response['store_name'] = y
                            for q in queryset:

                                data = {
                                    "store_name": q['items__item__store__store_name'],
                                    "order_id": q['order_id'],
                                    "amount": q['amount'],
                                    "choice": q['choice'],
                                    "payment_mode": q['payment_mode'],
                                    "created_at": q['created_at'],
                                }
                                final_response['data'].append(data)
                    return Response(final_response, status.HTTP_200_OK)
            except:
                return Response("some things went worng", status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

