from rest_framework import serializers
from product.models.category import Category_like

class Category_like_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category_like
        fields = (
            'category',
            'like',
                   )