from rest_framework import serializers
from product.models.Subcategory import Subcategory_like


class Subcategory_like_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory_like
        fields = (
            'user',
            'subcategory',
            'like',
                   )