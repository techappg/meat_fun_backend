from rest_framework import serializers, status

from backend_roc.utils.const import ORDER_OUT_FOR_DELIVERY, ORDER_READY
from product.models.address import Address
from product.models.cart import Cart
from product.models.order import Order, Transaction
import razorpay

from product.serializer.address_serializer import addressViewSerializer
from product.serializer.cart_serializer import CartViewSerializer
from product.serializer.product_serializer import ProductSerializer

# client = razorpay.Client(auth=("rzp_live_CbMRTtLiIOtCU6", "Uuv9j1vj3ccZHCbGMeIKJeBQ"))
from rocapi.interface.text_sms_interface import send_text

client = razorpay.Client(auth=("rzp_test_UxeO6rtAvoDjr0", "VTJklwITkvijiiQTYIw9sqSm"))


class order_Serializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    # billing_address = addressViewSerializer()
    shipping_address = addressViewSerializer()
    items = CartViewSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id',
                  'order_id',
                  'user',
                  'items',
                  'shipping_address',
                  # 'billing_address',
                  'amount',
                  'coupon',
                  'created_at',
                  'updated_at',
                  'order_status',
                  'status',
                  'delivery_time',
                  'mobile_num',
                  'choice',
                  'payment_mode',
                  )


class Transaction_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('razorpay_payment_id',
                  'razorpay_order_id',
                  'razorpay_signature',
                  )

class update_order_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id',
                  'status',
                  )

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        if instance.status == 'out for delivery' and instance.choice == 'Home Delivery':
            mobile = instance.mobile_num
            resp_status = send_text(mobile, ORDER_OUT_FOR_DELIVERY)
            #print(resp_status)
        if instance.status == 'out for delivery' and instance.choice == 'Picking':
            mobile = instance.mobile_num
            resp_status = send_text(mobile, ORDER_READY)
            #print(resp_status)
        return instance


class post_order_Serializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    time = serializers.TimeField(required=True)
    Choice = serializers.ChoiceField(required=True, choices=("Home Delivery", "Picking"))
    payment_mode = serializers.ChoiceField(required=True, choices=("COD", "ONLINE PAY"))
    coupon = serializers.CharField(required=False)
    store_id = serializers.IntegerField(required=True)


class id_store_id(serializers.Serializer):
    id = serializers.CharField(required=False)
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
