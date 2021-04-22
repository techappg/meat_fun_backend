from rest_framework.permissions import AllowAny, IsAuthenticated
from product.models.Subcategory import Subcategory_like
from rest_framework import viewsets

from product.serializer.Subcategory_like_serializer import Subcategory_like_Serializer


class Subcategory_like_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = Subcategory_like_Serializer
    queryset = Subcategory_like.objects.all()

