from rest_framework import serializers

from product.models.address import Address

class addressViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id','user','name','address_type', 'street_address', 'apartment_address', 'country','state',
                  'zip', 'city', 'mobile')

class update_addressViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('name','address_type', 'street_address', 'apartment_address', 'country',
                  'state','zip', 'city', 'mobile')

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.state = validated_data.get('state', instance.state)
            instance.address_type = validated_data.get('address_type', instance.address_type)
            instance.street_address = validated_data.get('street_address', instance.street_address)
            instance.apartment_address = validated_data.get('apartment_address', instance.apartment_address)
            instance.country = validated_data.get('country', instance.country)
            instance.city = validated_data.get('city', instance.city)
            instance.zip = validated_data.get('zip', instance.zip)
            instance.mobile = validated_data.get('mobile', instance.mobile)

            instance.save()
            return instance