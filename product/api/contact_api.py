from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.const import OWNER_EMAIL
from product.interface.send_email_owner import owner_send_email, file_send_email
from product.models.contact import Contact_us, Career
from product.serializer.contact_us_serializer import contact_serializers, Career_serializers


class Contact_ViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = contact_serializers
    queryset = Contact_us.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            contact = f"Name: {obj.name} <br> Email: {obj.email} <br> Contact no: {obj.mobile} <br> Message: {obj.contact}"
            resp_status = owner_send_email(contact, obj.title, OWNER_EMAIL)
            print(resp_status)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Career_ViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = Career_serializers
    queryset = Career.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            print(obj.cv)
            resp_status = file_send_email("Career Application", OWNER_EMAIL, obj.cv)
            print(resp_status)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)