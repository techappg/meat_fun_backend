from rest_framework import serializers


class RefundSerializer(serializers.Serializer):
    order_status = serializers.ChoiceField(required=True, choices=("order cancel",))
    order_id = serializers.CharField(required=True)