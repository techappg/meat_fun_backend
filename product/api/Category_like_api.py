from requests import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from product.models.category import Category_like
from product.serializer.Category_like_serializer import Category_like_Serializer
from rest_framework import viewsets

class Category_like_ViewSet(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Category_like_Serializer
    # queryset = Category_like.objects.all()
    def queryset(self):
        snippets = Category_like.objects.filter(user=self.request.user)
        serializer = Category_like_Serializer(snippets, many=True)
        return Response(serializer.data)

class Category_like_get_ViewSet(ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Category_like_Serializer
    def queryset(self):
        snippets = Category_like.objects.filter(user=self.request.user)
        serializer = Category_like_Serializer(snippets, many=True)
        return Response(serializer.data)