from django.shortcuts import get_object_or_404
from rest_framework import serializers
from product.models.products import Product, Images
from product.models.store import Store
from product.serializer.store_serializer import get_store_Serializer
import random


class Images_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = (
            'id',
            'product',
            'image'
        )


class ProductSerializer(serializers.ModelSerializer):
    images = Images_Serializer(many=True, source="product_images")
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    category_name = serializers.SerializerMethodField(method_name='get_category_name')
    subcategory_name = serializers.SerializerMethodField(method_name='get_subcategory_name',default=None )
    default_image = serializers.SerializerMethodField(method_name='get_default_image')
    store = get_store_Serializer()

    class Meta:
        model = Product
        fields = (  'id',
                    'category',
                    'category_name',
                    'subcategory',
                    'subcategory_name',
                    'name',
                    'price',
                    'MRP',
                    'quantity',
                    'quantity_type',
                    'discount',
                    'tax_CGST',
                    'tax_SGST',
                    'default_image',
                    'images',
                    'description',
                    'Enable',
                    'keyword',
                    'productUsage',
                    'store',
                    'master_key',
                    'product_code',
                    'seo_title',
                    'created_at',
                    'updated_at',
                    )

    def get_category_name(self, obj):
        return obj.category.name

    def get_subcategory_name(self, obj):
        if obj.subcategory:
            return obj.subcategory.name
        else:
            return None

    def get_default_image(self, obj):
        if obj.default_image:
            return self.context["request"].build_absolute_uri(obj.default_image.url)
        return None

    def get_images(self, obj):
        if obj.images:
            return self.context["request"].build_absolute_uri(obj.images.url)
        return None


class addProductSerializer(serializers.ModelSerializer):
    # images = Images_Serializer(required=False)
    store_id = serializers.ListField(default=None, write_only=True, required=False)
    images = serializers.ListField(required=False,
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=True,
                                    use_url=False)
    )

    price = serializers.DecimalField(decimal_places=2, max_digits=10, required=True)

    class Meta:
        model = Product
        fields = (
                    'category',
                    'subcategory',  
                    'name',
                    'price',
                    'MRP',
                    'quantity',
                    'quantity_type',
                    'discount',
                    'tax_CGST',
                    'tax_SGST',
                    'Enable',
                    'default_image',
                    'images',
                    'keyword',
                    'productUsage',
                    'description',
                    'store_id',
                    'product_code',
                    'seo_title',
                    )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        store_id = validated_data.get('store_id')
        master_key = random.randint(1000, 9999)
        # store_id = "1,2"
        if store_id:
            sstoreid = store_id[0].split(",")
            for stores in sstoreid:
                p_store = Store.objects.get(id=stores)
                product = Product.objects.create(
                                                 category=validated_data.get('category'),
                                                 subcategory=validated_data.get('subcategory'),
                                                 name=validated_data.get('name'),
                                                 price=validated_data.get('price'),
                                                 MRP=validated_data.get('MRP'),
                                                 quantity=validated_data.get('quantity'),
                                                 quantity_type=validated_data.get('quantity_type'),
                                                 discount=validated_data.get('discount'),
                                                 tax_CGST=validated_data.get('tax_CGST'),
                                                 tax_SGST=validated_data.get('tax_SGST'),
                                                 Enable=validated_data.get('Enable'),
                                                 keyword=validated_data.get('keyword'),
                                                 default_image=validated_data.get('default_image'),
                                                 description=validated_data.get('description'),
                                                 productUsage=validated_data.get('productUsage'),
                                                 store=p_store,
                                                 master_key=master_key,
                                                 product_code=validated_data.get('product_code'),
                                                 seo_title=validated_data.get('seo_title'),
                                                 )
        else:
            product = Product.objects.create(
                                                 category=validated_data.get('category'),
                                                 subcategory=validated_data.get('subcategory'),
                                                 name=validated_data.get('name'),
                                                 price=validated_data.get('price'),
                                                 MRP=validated_data.get('MRP'),
                                                 quantity=validated_data.get('quantity'),
                                                 quantity_type=validated_data.get('quantity_type'),
                                                 discount=validated_data.get('discount'),
                                                 tax_CGST=validated_data.get('tax_CGST'),
                                                 tax_SGST=validated_data.get('tax_SGST'),
                                                 Enable=validated_data.get('Enable'),
                                                 keyword=validated_data.get('keyword'),
                                                 default_image=validated_data.get('default_image'),
                                                 description=validated_data.get('description'),
                                                 productUsage=validated_data.get('productUsage'),
                                                 master_key=master_key,
                                                 product_code=validated_data.get('product_code'),
                                                 seo_title=validated_data.get('seo_title'),
                                                )

        # images = validated_data.get('images')
        # print(images)

        if images_data.getlist("images"):
            for image in images_data.getlist("images"):
                Images.objects.create(product=product, image=image)
        return product


class UpdateProductSerializer(serializers.ModelSerializer):
    images = Images_Serializer(many=True, source="product_images")
    category_name = serializers.SerializerMethodField(method_name='get_category_name')
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    default_image = serializers.FileField(required=False)
    master_key = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = (  
                    'id',
                    'category',
                    'category_name',
                    'subcategory',                    
                    'name',
                    'price',
                    'MRP',
                    'quantity',
                    'quantity_type',
                    'discount',
                    'tax_CGST',
                    'tax_SGST',
                    'Enable',
                    'images',
                    'default_image',
                    'keyword',
                    'productUsage',
                    'description',
                    # 'store',
                    'created_at',
                    'updated_at',
                    'master_key',
                    'product_code',
                    'seo_title',
                    )

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES
        master_key = validated_data.get('master_key', instance.master_key)
        # print(master_key)
        # update_products = Product.objects.filter(master_key=master_key).update(
        #     category=validated_data.get('category', instance.category),
        #     subcategory=validated_data.get('subcategory', instance.subcategory),
        #     name=validated_data.get('name', instance.name),
        #     price=validated_data.get('price', instance.price),
        #     MRP=validated_data.get('MRP', instance.MRP),
        #     description=validated_data.get('description', instance.description),
        #     tax_CGST=validated_data.get('tax_CGST', instance.tax_CGST),
        #     tax_SGST=validated_data.get('tax_SGST', instance.tax_SGST),
        #     Enable=validated_data.get('Enable', instance.Enable),
        #     keyword=validated_data.get('keyword', instance.keyword),
        #     default_image=validated_data.get('default_image', instance.default_image),
        #     productUsage=validated_data.get('productUsage', instance.productUsage),
        #     product_code=validated_data.get('product_code', instance.product_code),
        # )

        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.MRP = validated_data.get('MRP', instance.MRP)
        instance.description = validated_data.get('description', instance.description)
        instance.tax_CGST = validated_data.get('tax_CGST', instance.tax_CGST)
        instance.tax_SGST = validated_data.get('tax_SGST', instance.tax_SGST)
        instance.Enable = validated_data.get('Enable', instance.Enable)
        instance.keyword = validated_data.get('keyword', instance.keyword)
        instance.default_image = validated_data.get('default_image', instance.default_image)
        instance.images = validated_data.get('images', instance.product_images)
        instance.productUsage = validated_data.get('productUsage', instance.productUsage)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.quantity_type = validated_data.get('quantity_type', instance.quantity_type)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.seo_title = validated_data.get('seo_title', instance.seo_title)

        instance.save()

        pro_update = Product.objects.filter(master_key=master_key)
        if images_data.getlist("images"):
            for user in pro_update:
                image = Images.objects.filter(product=user)
                for img in image:
                    img.delete()

        for image in images_data.getlist("images"):
            for user in pro_update:
                Images.objects.create(product=user, image=image)
        return instance

    def get_category_name(self, obj):
        return obj.category.name


class Update_store_products_Serializer(serializers.ModelSerializer):
    images = Images_Serializer(many=True, source="product_images")
    category_name = serializers.SerializerMethodField(method_name='get_category_name')
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    default_image = serializers.FileField(required=False)
    master_key = serializers.CharField(read_only=True)
    store = get_store_Serializer(read_only=True)

    class Meta:
        model = Product
        fields = (
                    'id',
                    'category',
                    'category_name',
                    'subcategory',
                    'name',
                    'price',
                    'MRP',
                    'quantity',
                    'quantity_type',
                    'discount',
                    'tax_CGST',
                    'tax_SGST',
                    'default_image',
                    'images',
                    'Enable',
                    'store',
                    'keyword',
                    'productUsage',
                    'description',
                    'created_at',
                    'updated_at',
                    'master_key',
                    'product_code',
                    'seo_title',
                    )

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.MRP = validated_data.get('MRP', instance.MRP)
        instance.description = validated_data.get('description', instance.description)
        instance.tax_CGST = validated_data.get('tax_CGST', instance.tax_CGST)
        instance.tax_SGST = validated_data.get('tax_SGST', instance.tax_SGST)
        instance.Enable = validated_data.get('Enable', instance.Enable)
        instance.keyword = validated_data.get('keyword', instance.keyword)
        instance.default_image = validated_data.get('default_image', instance.default_image)
        instance.images = validated_data.get('images', instance.product_images)
        instance.productUsage = validated_data.get('productUsage', instance.productUsage)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.quantity_type = validated_data.get('quantity_type', instance.quantity_type)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.seo_title = validated_data.get('seo_title', instance.seo_title)
        instance.save()

        # images = validated_data.get('images', instance.images)
        images_data = self.context.get('view').request.FILES
        # print(images)

        if images_data.getlist("images"):
            image = Images.objects.filter(product=instance)
            for img in image:
                img.delete()

            for image in images_data.getlist("images"):
                Images.objects.create(product=instance, image=image)

        # for image in images_data.getlist("images"):
        #     Images.objects.create(product=instance, image=image)
        return instance

    def get_category_name(self, obj):
        return obj.category.name


class PosEnable(serializers.Serializer):
    Enable_disenable = serializers.BooleanField()
