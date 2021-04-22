from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from blog.models.blog import blog_Category
from blog.serializer.category_serializer import category_serilazer

class Category_ViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = category_serilazer
    queryset = blog_Category.objects.all()
