from django.contrib.auth.models import User
from rest_framework import serializers
from product.models.rating import Rating, Review


class Rating_serilazer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'product', 'product_rating', 'created_at', 'updated_at')

class Review_serilazer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'product', 'product_review', 'created_at', 'updated_at')

