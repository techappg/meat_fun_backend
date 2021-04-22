from django.contrib.auth.models import User
from requests import Response

from product.models.address import Address
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from product.serializer.address_serializer import addressViewSerializer, update_addressViewSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class Address_View(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = addressViewSerializer
    queryset = Address.objects.all()

class Update_Address_View(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = update_addressViewSerializer
    queryset = Address.objects.all()

class Get_Address_View(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = addressViewSerializer
    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)
