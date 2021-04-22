from rest_framework import serializers
from product.models.store import Store


class store_Serializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Store
        fields = ('id', 'store_name', 'state', 'city', 'address', 'latitude', 'longitude', 'storeId', 'is_enable',
                  'MERCHANT_KEY', 'MID', 'created_at', 'updated_at')


class get_store_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('id', 'store_name', 'state', 'city', 'address', 'latitude', 'longitude', 'storeId', 'is_enable', 'MERCHANT_KEY', 'MID')