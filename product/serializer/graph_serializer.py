from datetime import timedelta

from rest_framework import serializers


class Count_Serializer(serializers.Serializer):
    start_date = serializers.CharField(required=False)
    end_data = serializers.CharField(required=False)


class StoreMonthSaleSerializer(serializers.Serializer):
    store_id = serializers.CharField(required=False)
