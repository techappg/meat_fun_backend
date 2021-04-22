# from product.models import Subcategory

from rest_framework import serializers

from product.models.Subcategory import Subcategory
from product.models.category import Category


class subcategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S',read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'category',
            'created_at',
            'updated_at',
        )


class InputSubcategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'is_enable', 'created_at', 'updated_at']


class InputSubcategorySerializer1(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    category_name = serializers.SerializerMethodField(method_name='get_category_name')
    category_image = serializers.SerializerMethodField(method_name='get_category_image')

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category_name', 'category_image', 'is_enable', 'created_at', 'updated_at']

    def get_category_name(self, obj):
        return obj.category.name

    def get_category_image(self, obj):
        if obj.category.image:
            return self.context["request"].build_absolute_uri(obj.category.image.url)
        return None
