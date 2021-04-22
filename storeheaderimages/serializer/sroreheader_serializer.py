from rest_framework import serializers

from product.serializer.store_serializer import get_store_Serializer
from storeheaderimages.models import Storeheader


class StoreHeaderImageSerializer(serializers.ModelSerializer):
    store_id_list = serializers.CharField(required=True)

    class Meta:
        model = Storeheader
        fields = ('id', 'name', 'image', 'default_image', 'is_enable', 'store_id_list' )


class StoreHeaderImageSerializerGet(serializers.ModelSerializer):
    store = get_store_Serializer()
    image = serializers.SerializerMethodField(method_name='get_default_image')

    class Meta:
        model = Storeheader
        fields = ('id', 'name', 'image', 'default_image', 'is_enable', 'store',)

    def get_default_image(self, obj):
        if obj.image:
            return self.context["request"].build_absolute_uri(obj.image.url)
        return None


class StoreHeaderImageSerializerPatch(serializers.ModelSerializer):
    pos_store_id = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Storeheader
        fields = ('id', 'name', 'image', 'default_image', 'is_enable', 'store', 'pos_store_id')