from backend_roc.utils.permissions import Is_admin
from product.models.Subcategory import Subcategory
from product.serializer.subcategory_serializer import InputSubcategorySerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from rest_framework import status
from rest_framework.response import Response


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SubcategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [Is_admin,]
    serializer_class = InputSubcategorySerializer
    queryset = Subcategory.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        category = self.queryset.get(id=pk)
        serializer = InputSubcategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = self.queryset.get(id=pk)
        serializer = InputSubcategorySerializer(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            category.refresh_from_db()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)