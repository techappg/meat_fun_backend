import random

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc import PaytmChecksum
from backend_roc.utils.const import ORDER_CANCEL
from product.models.order import Order
from product.models.store import Store
from product.serializer.pytem_refund_serializer import RefundSerializer
import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
from product.utils.encryption_decryption import decrypt
from rocapi.interface.text_sms_interface import send_text

from datetime import datetime


class PaytmRefund(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RefundSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_status = serializer.data.get('order_status')
            order_id = serializer.data.get('order_id')

            try:
                order = Order.objects.get(order_id=order_id)
                txnId = order.txnId
                amount = order.amount
                store_id = order.store_id

                store = Store.objects.get(storeId=store_id)
                MERCHANT_KEY = decrypt(store.MERCHANT_KEY)
                MID = decrypt(store.MID)
            except:
                response_data = dict()
                data = {
                    'msg': "order id dose not exists"
                }
                response_data['data'] = data
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if order.status == 'successfully delivered':
                response_data = dict()
                data = {
                    'msg': "delivered order dose not canceled"
                }
                response_data['data'] = data
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            order_date = order.created_at.strftime("%Y/%m/%d")
            today_date = datetime.now().strftime("%Y/%m/%d")

            if today_date != order_date:
                response_data = dict()
                data = {
                    'msg': "old order dose not canceled"
                }
                response_data['data'] = data
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if order.payment_mode == 'COD':
                if order.status == "order cancel":
                    response_data = dict()
                    data = {
                        'msg': "order already canceled"
                    }
                    response_data['data'] = data
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                order.status = order_status
                order.save()
                mobile_num = order.mobile_num
                final_msg = ORDER_CANCEL.replace("<order_id>", str(order_id))
                resp_status = send_text(mobile_num, final_msg)
                response_data = dict()
                data = {
                    'msg': "order successfully canceled"
                }
                response_data['data'] = data
                return Response(response_data, status=status.HTTP_200_OK)

            REFUNDID_ID = random.randint(10000000, 99999999)

            paytmParams = dict()
            paytmParams["body"] = {
                "mid": MID,
                "txnType": "REFUND",
                "orderId": order_id,
                "txnId": txnId,
                # "refId": "REFUNDID_98765",
                "refId": str(REFUNDID_ID),
                "refundAmount": str(amount),
            }

            # Generate checksum by parameters we have in body
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)

            paytmParams["head"] = {
                "signature": checksum
            }

            post_data = json.dumps(paytmParams)

            # for Staging
            # url = "https://securegw-stage.paytm.in/refund/apply"

            # for Production
            url = "https://securegw.paytm.in/refund/apply"

            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            print(response)
            if response['body']['resultInfo']['resultCode'] == '601':
                order.status = order_status
                order.save()
                mobile_num = order.mobile_num
                final_msg = ORDER_CANCEL.replace("<order_id>", str(order_id))
                resp_status = send_text(mobile_num, final_msg)
                response_data = dict()
                data = {
                    'msg': "order successfully canceled"
                }
                response_data['data'] = data
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = dict()
                data = {
                    'msg': "order already canceled"
                }
                response_data['data'] = data
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
