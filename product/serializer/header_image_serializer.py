from product.models import header_image
from product.models.header_image import header_image
from rest_framework import serializers

class header_imageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)
    is_enable = serializers.BooleanField(default=True)
    class Meta:
        model = header_image
        fields = ('id', 'name', 'image', 'default_image', 'is_enable')

    def create(self, validated_data):
        if validated_data['default_image'] == True :
            queryset = header_image.objects.all().update(default_image=False)
            qyset = header_image.objects.create(**validated_data)
            return qyset
        else:
            qyset = header_image.objects.create(**validated_data)
            return qyset

    def update(self, instance, validated_data):
        if validated_data['default_image'] == True :
            queryset = header_image.objects.all().update(default_image=False)
            instance.name = validated_data.get('name', instance.name)
            instance.image = validated_data.get('image', instance.image)
            instance.default_image = validated_data.get('default_image', instance.default_image)
            instance.is_enable = validated_data.get('is_enable', instance.is_enable)
            instance.save()
        else:
            instance.name = validated_data.get('name', instance.name)
            instance.image = validated_data.get('image', instance.image)
            instance.default_image = validated_data.get('default_image', instance.default_image)
            instance.is_enable = validated_data.get('is_enable', instance.is_enable)
            instance.save()
        return instance

