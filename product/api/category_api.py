from backend_roc.utils.permissions import Is_admin
from product.models.category import Category
from product.models.Subcategory import Subcategory
from product.models.order import Order
from product.models.products import Product
from product.serializer.Category_serializer import CategorySerializer, InputCategorySerializer
from product.serializer.subcategory_serializer import InputSubcategorySerializer1
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from rest_framework.parsers import MultiPartParser, FileUploadParser


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [Is_admin, ]
    serializer_class = InputCategorySerializer
    queryset = Category.objects.all()
    parser_classes = [MultiPartParser, FileUploadParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # if there is subcategory corresponding to category)
        try:
            c = Subcategory.objects.filter(category_id=pk)
        except Subcategory.DoesNotExist:
            msg = "No record found"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        if c:
            serializer = InputSubcategorySerializer1(c, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = "No record found"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        # if there is no subcategory corresponding to category
        # c1 = self.queryset.filter(id=pk)
        # if c1:
        #     serializer1 = self.serializer_class(c1, many=True)
        #     return Response(serializer1.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        category = self.queryset.get(id=pk)
        serializer = InputCategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = self.queryset.get(id=pk)
        serializer = InputCategorySerializer(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            category.refresh_from_db()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            id = self.kwargs['pk']
            category = Category.objects.get(id=id)
            order = Product.objects.filter(category=category)
            print(order)
            if order.exists():
                return Response("category have Product please do not delete category use enable disable ", status=status.HTTP_400_BAD_REQUEST)
            category.delete()
            return Response("delete successfully ", status=status.HTTP_200_OK)
        except:
            return Response("id dose not exists please check your id ", status=status.HTTP_400_BAD_REQUEST)