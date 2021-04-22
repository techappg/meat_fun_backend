from django.contrib.auth.models import User
from rest_framework import serializers
from product.models.booklet import Booklet


class Booklet_Serializer(serializers.ModelSerializer):
    booklet_no = serializers.ListField(write_only=True)
    booklet_number = serializers.CharField(source="booklet_no", read_only=True)
    class Meta:
        model = Booklet
        fields = ('perfix','booklet_no', 'booklet_number')

    def create(self, validated_data):
        booklet_no = validated_data['booklet_no']
        user = self.context["request"].user
        for code in booklet_no:
            book = Booklet.objects.create(user=user, booklet_no=code, perfix=validated_data.get('perfix'),)
        return book
