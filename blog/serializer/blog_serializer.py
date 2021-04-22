from rest_framework import serializers
from blog.models.blog import Blog


class Blog_serilazer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'category', 'title', 'description', 'image', 'image_positions', 'is_enable', 'created_at', 'updated_at')