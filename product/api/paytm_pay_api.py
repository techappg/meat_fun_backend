import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
# import PaytmChecksum
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from backend_roc import PaytmChecksum
from backend_roc.utils.const import POS_MACHINE_API
from product.models.address import Address
from product.models.cart import Cart
from product.models.order import Order
from product.models.store import Store
from product.serializer.paytm_serializer import PaytmSerializer, StatusPaytmSerializer, callStatusPaytmSerializer
from product.utils.encryption_decryption import decrypt


class PaytemProductView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PaytmSerializer

    def post(self, request):
        serializer = PaytmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # testing
            # MERCHANT_KEY = 'C&V90TEOpYcXIiWT'
            # MID = 'STARFO99000157018897'

            # live
            # MERCHANT_KEY = '#O3h7F5V_UVrwZj1'
            # MID = 'STARFO09924218952868'

            MERCHANT_KEY = serializer.data.get('MERCHANT_KEY')
            MID = serializer.data.get('MID')

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
                pass
            else:
                final_response = dict()
                final_response['error'] = True
                data = {
                    "MSG": "Empty cart"
                }
                final_response['data'] = data
                return Response(final_response, status=status.HTTP_400_BAD_REQUEST)

            if order_qs.exists():
                order_qs.delete()
                order = Order.objects.create(user=user, order_status=False, store_id=store_id,)
                items = order.items
                for item in cart:
                    items.add(item)
                order.save()
            else:
                order = Order.objects.create(user=user, order_status=False, store_id=store_id, )
                items = order.items
                for item in cart:
                    items.add(item)
                order.save()

            real_amount = float(order_qs[0].get_total())
            print('amount', real_amount)

            # list1 = []
            order_id = ''
            for qs in order_qs:
                order_id += (str(qs.id))

            # for qs in order_qs:
            #     list1.append(qs.id)
            # order_id = ''.join(str(e) for e in list1)
            # print(order_id)

            if payment_mode == "COD" and Choice == 'Picking':
                order_qs.update(order_id=order_id,
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
                order_qs.update(order_id=order_id,
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
                final_response = dict()
                final_response['error'] = False
                data = {
                    "order_id": order_id,
                    "amount": real_amount,
                }
                final_response['data'] = data
                return Response(final_response, status.HTTP_200_OK)

            if payment_mode == "ONLINE PAY" and Choice == 'Home Delivery':
                try:
                    shipping_address = Address.objects.get(user=user, address_type="Shipping")
                except:
                    return Response("Address Dose not exists", status=status.HTTP_400_BAD_REQUEST)
                order_qs.update(order_id=order_id,
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
                order_qs.update(order_id=order_id,
                                amount=real_amount,
                                delivery_time=time,
                                mobile_num=mobile,
                                choice=Choice,
                                )

            paytmParams = dict()
            paytmParams["body"] = {
                "requestType": "Payment",
                "mid": MID,
                "websiteName": "WEBSTAGING",
                "orderId": str(order_id),
                # "callbackUrl": "https://merchant.com/callback",
                "callbackUrl": "https://api.meat.fun/product/callback",
                "txnAmount": {
                    "value": str(real_amount),
                    "currency": "INR",
                },
                "userInfo": {
                    "custId": "CUST_001",
                },
            }

            # Generate checksum by parameters we have in body
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)

            paytmParams["head"] = {
                "signature": checksum
            }

            post_data = json.dumps(paytmParams)

            # for Staging
            # url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=<mid>&orderId=<order_id>"
            # url = url.replace('<mid>', MID)
            # url = url.replace('<order_id>', order_id)
            # print(url)

            # for Production
            url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=<mid>&orderId=<order_id>"
            url = url.replace('<mid>', MID)
            url = url.replace('<order_id>', order_id)

            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            print(response)

            response_data = {
                'order_id': order_id,
                'response': response
            }
            return Response(response_data, status=status.HTTP_200_OK)


class CallBackView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = StatusPaytmSerializer

    def post(self, request):
        serializer = StatusPaytmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            resp_data = request.data
            response_dict = {}
            for data in resp_data:
                response_dict[data] = resp_data[data]
            ORDERID = response_dict['ORDERID']
            #returnurl = "http://localhost:3000/payment-confirmation/<order_id>"
            returnurl = "https://meat.fun/payment-confirmation/<order_id>"
            returnurl = returnurl.replace('<order_id>', ORDERID)
            return HttpResponseRedirect(redirect_to=returnurl)


class StatusPaytemProductView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = callStatusPaytmSerializer

    def post(self, request):
        serializer = callStatusPaytmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # order_id = serializer.data.get('order_id')
            # store_id = serializer.data.get('store_id')

            user = self.request.user
            order_qs = Order.objects.filter(user=user, order_status=False)
            store_id = 0
            order_id = ''

            for data in order_qs:
                if store_id == 0:
                    store_id += data.store_id
                    order_id += (str(data.order_id))

            cart = Cart.objects.filter(user=user, ordered=False, store_id=store_id)
            print(cart)
            try:
                store = Store.objects.get(storeId=store_id)
                MERCHANT_KEY = decrypt(store.MERCHANT_KEY)
                MID = decrypt(store.MID)
            except:
                return Response("store dose not exists", status=status.HTTP_400_BAD_REQUEST)

            paytmParams = dict()

            # body parameters
            paytmParams["body"] = {

                # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                "mid": MID,

                # Enter your order id which needs to be check status for
                "orderId": str(order_id),
            }

            # Generate checksum by parameters we have in body
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)

            # head parameters
            paytmParams["head"] = {

                # put generated checksum value here
                "signature": checksum
            }

            # prepare JSON string for request
            post_data = json.dumps(paytmParams)

            # for Staging
            # url = "https://securegw-stage.paytm.in/v3/order/status"

            # for Production
            url = "https://securegw.paytm.in/v3/order/status"

            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            print(response)
            response_dict = {}
            for qs in response.keys():
                response_dict[qs] = response[qs]

            print(response_dict['body']['resultInfo']['resultCode'])

            if response_dict['body']['resultInfo']['resultCode'] == "01":
                txnId = response_dict['body']['txnId']
                bankTxnId = response_dict['body']['bankTxnId']

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
                    responce_data['TotalAmount'] = float(qs.amount)
                    if qs.payment_mode == 'COD':
                        responce_data['PayMode'] = 1
                        responce_data['TotalAmountPaid'] = 0
                    else:
                        responce_data['PayMode'] = 7
                        responce_data['TotalAmountPaid'] = float(qs.amount)
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

                if send.status_code == 201:
                    print(send.content)
                    cart.update(ordered=True)
                    order_qs.update(order_status=True, txnId=txnId, bankTxnId=bankTxnId)
            return Response(response, status=status.HTTP_200_OK)
            # return Response("test", status=status.HTTP_200_OK)
