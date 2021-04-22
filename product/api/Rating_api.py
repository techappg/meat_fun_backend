from rest_framework import viewsets, generics, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from product.models.order import Order
from product.models.products import Product
from product.models.rating import Rating, Review
from product.serializer.Rating_serializer import Rating_serilazer, Review_serilazer
from rest_framework import exceptions


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class rating_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated|ReadOnly, ]
    serializer_class = Rating_serilazer
    queryset = Rating.objects.all()

    def create(self, request,  *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        product = validated_data["product"]
        order = Order.objects.filter(items__item__id=product.id, order_status=True, user=self.request.user)
        if order.exists():
            validated_data["user"] = request.user
            serializer.create(validated_data=validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("order first", status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            products = Product.objects.get(id=pk)
            queryset = Rating.objects.get(user=self.request.user, product=products)
        except Product.DoesNotExist:
            raise exceptions.NotFound(detail="id dose not exists")

        serializer = Rating_serilazer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Rating.objects.filter(user=self.request.user, product__id=pk)
        serializer = Rating_serilazer(queryset, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    # def list(self, request, pk=None):
    #     print("pk",pk)
    #     products = Product.objects.get(id=138)
    #     queryset = Rating.objects.filter(product=products)
    #     serializer = Rating_serilazer(queryset, many=True)
    #     return Response(serializer.data, status.HTTP_200_OK)


class Review_ViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny|ReadOnly, ]
    serializer_class = Review_serilazer
    queryset = Review.objects.all()

    def create(self, request,  *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        product = validated_data["product"]
        order = Order.objects.filter(items__item__id=product.id, order_status=True, user=self.request.user)
        if order.exists():
            validated_data["user"] = request.user
            serializer.create(validated_data=validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("order first", status=status.HTTP_400_BAD_REQUEST)

class Rating_count_View(ListAPIView):
    permission_classes = [AllowAny, ]

    def list(self, request, product_id, star=None):
        try:
            product = Product.objects.get(id=product_id)
            queryset = Rating.objects.filter(product=product, product_rating=star).count()
            final_response = dict()
            data = {
                "user": queryset,
            }
            final_response['data'] = data
            return Response(queryset, status.HTTP_200_OK)
        except:
            return Response("product dose not exists", status.HTTP_400_BAD_REQUEST)

class Rating_get_count_View(ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def list(self, request, product_id=None):
        # try:
        id = self.kwargs['product_id']
        queryset = Rating.objects.filter(product__id=id, user=self.request.user)
        serializer = Rating_serilazer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
        # except:
        #     return Response("product dose not exists", status.HTTP_400_BAD_REQUEST)
