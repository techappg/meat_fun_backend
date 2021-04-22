from product.models.category import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class InputCategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "image", "is_enable","meta_title", "meta_description", "created_at", "updated_at")

    def get_image(self, obj):
        if obj.image:
            return self.context["request"].build_absolute_uri(obj.image.url)
        return None




