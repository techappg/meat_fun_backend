from rest_framework import serializers
from product.models.contact import Contact_us, Career


class contact_serializers(serializers.ModelSerializer):
    class Meta:
        model = Contact_us
        fields = ('id', 'name', 'email', 'mobile', 'title', 'contact')

class Career_serializers(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'