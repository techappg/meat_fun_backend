# from product.models import Cart
from product.models.cart import Cart
from rest_framework import serializers
from product.serializer.product_serializer import ProductSerializer


class CartViewSerializer(serializers.ModelSerializer):
    item = ProductSerializer()

    class Meta:
        model = Cart
        fields = (
                    'id',
                    'item',
                    'quantity',
                    'get_total_item_price',
                    # 'get_discount',
                    # 'get_tax_CGST',
                    # 'get_tax_SGST',
                    'get_final_amount',
                  )


class Cart_update_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id',
                    'item',
                    'quantity', )

    def update(self, instance, validated_data):
        instance.item = validated_data.get('item', instance.item)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class Cart_create_Serializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1, required=False)
    store_id = serializers.IntegerField(required=True)

    class Meta:
        model = Cart
        fields = ('id', 'item', 'quantity', 'store_id')