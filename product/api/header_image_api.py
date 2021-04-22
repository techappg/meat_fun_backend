from requests import Response

from backend_roc.utils.permissions import Is_admin
from product.models.header_image import header_image
from product.serializer.header_image_serializer import header_imageSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class header_imageViewSet(viewsets.ModelViewSet):
    permission_classes = [Is_admin|ReadOnly, ]
    serializer_class = header_imageSerializer

    def get_queryset(self):
        snippets = header_image.objects.all()
        return snippets
