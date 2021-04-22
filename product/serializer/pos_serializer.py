from rest_framework import serializers


class PosProductPostSerializer(serializers.Serializer):
    ItemName = serializers.CharField(required=True)
    ItemType = serializers.CharField(required=True)
    ItemCategory = serializers.CharField(required=True)
    itemPrice = serializers.CharField(required=True)
    # OutletId = serializers.CharField(required=True)
    taxid = serializers.CharField(required=True)

    subcategory = serializers.CharField(required=False)
    category = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.CharField(required=True)
    quantity_type = serializers.CharField(required=True)
    productUsage = serializers.CharField(required=True)
    keyword = serializers.CharField(required=True)

    store = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)

    default_image = serializers.FileField(required=True)

    Enable = serializers.BooleanField(default=True)
    seo_title = serializers.CharField(required=True)


