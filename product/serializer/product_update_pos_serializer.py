from rest_framework import serializers


class PosProductSerializer(serializers.Serializer):
    product_code = serializers.CharField(required=True)
    store_id = serializers.CharField(required=False)
    price = serializers.FloatField(required=True)