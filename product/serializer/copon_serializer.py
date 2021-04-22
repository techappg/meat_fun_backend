from rest_framework import serializers
from product.models.booklet import Booklet
from product.models.coupon import Coupon
from django.contrib.auth.models import User

# class couponViewSerializer(serializers.ModelSerializer):
#     start_offer_time = serializers.DateField(required=True)
#     end_offer_time = serializers.DateField(required=True)
#     order_persent = serializers.IntegerField(max_value=None, min_value=None, required=True)
#     minimum_amount = serializers.IntegerField(max_value=None, min_value=None, required=True)
#     number_of_coupon = serializers.IntegerField(max_value=None, min_value=None, required=True)
#     perfix_no = serializers.CharField(required=True, write_only=True)
#     coupon_code = serializers.ListField(write_only=True)
#     code = serializers.CharField(source="coupon_code", read_only=True)
#     class Meta:
#         model = Coupon
#         fields = ('subcategory', 'category', 'product',
#                   'start_offer_time', 'end_offer_time', 'number_of_coupon', 'order_persent',
#                   'minimum_amount', 'coupon_code', 'code', 'perfix_no')
#
#     def create(self, validated_data):
#         coupon = validated_data['coupon_code']
#         perfix_no = validated_data['perfix_no']
#         PerFix = Booklet.objects.filter(perfix=perfix_no)
#         print("code ", PerFix)
#         for booklet in PerFix:
#             for code in coupon:
#                 coupon_coupon = Coupon.objects.create(
#                                                     subcategory=validated_data.get('subcategory'),
#                                                     category=validated_data.get('category'),
#                                                     product=validated_data.get('product'),
#                                                     booklet=booklet,
#                                                     start_offer_time=validated_data.get('start_offer_time'),
#                                                     end_offer_time=validated_data.get('end_offer_time'),
#                                                     number_of_coupon=validated_data.get('number_of_coupon'),
#                                                     order_persent=validated_data.get('order_persent'),
#                                                     minimum_amount=validated_data.get('minimum_amount'),
#                                                     coupon_code=code,
#                                                                                         )
#         return coupon_coupon
#
#
#     def update(self, instance, validated_data):
#         instance.subcategory = validated_data.get('subcategory', instance.subcategory)
#         instance.category = validated_data.get('category', instance.category)
#         instance.product = validated_data.get('product', instance.product)
#         instance.booklet = validated_data.get('booklet', instance.booklet)
#         instance.start_offer_time = validated_data.get('start_offer_time', instance.start_offer_time)
#         instance.end_offer_time = validated_data.get('end_offer_time', instance.end_offer_time)
#         instance.number_of_coupon = validated_data.get('number_of_coupon', instance.number_of_coupon)
#         instance.order_persent = validated_data.get('order_persent', instance.order_persent)
#         instance.minimum_amount = validated_data.get('minimum_amount', instance.minimum_amount)
#         instance.coupon_code = validated_data.get('coupon_code', instance.coupon_code)
#         instance.save()
#         return instance
#
class coupon_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ('subcategory', 'category', 'coupon_code', 'store',
                  'number_of_coupon', 'coupon_for', 'product_master_key', 'minimum_amount',
                  'discount_percent', 'discount_amount')

class apply_coupon_Serializer(serializers.Serializer):
    add_coupon = serializers.CharField(required=True)
