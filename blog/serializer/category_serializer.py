from rest_framework import serializers
from blog.models.blog import blog_Category


class category_serilazer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = blog_Category
        fields = ('id', 'name', 'created_at', 'updated_at')