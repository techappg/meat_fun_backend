from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny
from rest_framework.response import Response

from backend_roc.utils.const import OWNER_EMAIL
from feedback.models.feedback import Feedback
from feedback.serializer.feedback_serializer import FeedBackSerializer
from product.interface.send_email_owner import owner_send_email


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class FeedBackViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    serializer_class = FeedBackSerializer
    queryset = Feedback.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            contact = f"Name: {obj.name} <br> Email: {obj.email} <br> Message: {obj.massages}"
            resp_status = owner_send_email(contact, "Feedback", OWNER_EMAIL)
            print(resp_status)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        category = self.queryset.get(id=pk)
        serializer = FeedBackSerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = self.queryset.get(id=pk)
        serializer = FeedBackSerializer(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            category.refresh_from_db()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)