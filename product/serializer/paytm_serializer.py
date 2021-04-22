from rest_framework import serializers


class PaytmSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    time = serializers.TimeField(required=True)
    Choice = serializers.ChoiceField(required=True, choices=("Home Delivery", "Picking"))
    payment_mode = serializers.ChoiceField(required=True, choices=("COD", "ONLINE PAY"))
    coupon = serializers.CharField(required=False)
    store_id = serializers.IntegerField(required=True)
    MERCHANT_KEY = serializers.CharField(required=True)
    MID = serializers.CharField(required=True)


class StatusPaytmSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=False)
    # store_id = serializers.IntegerField(required=True)


class callStatusPaytmSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=False)
    store_id = serializers.IntegerField(required=False)