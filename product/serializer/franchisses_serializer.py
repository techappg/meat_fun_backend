from rest_framework import serializers
from product.models.franchisses import Franchisses


class franchissesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Franchisses
        fields = ('id', 'name', 'city', 'mobile_no', 'message')