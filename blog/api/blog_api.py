from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from blog.models.blog import Blog
from blog.serializer.blog_serializer import Blog_serilazer

class blog_ViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = Blog_serilazer
    queryset = Blog.objects.all()


class blog_user_ViewSet(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Blog_serilazer
    def get_queryset(self):
        queryset = Blog.objects.filter(is_enable=True)
        return queryset
