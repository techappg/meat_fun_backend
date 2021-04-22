from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from datetime import date, timezone, timedelta, datetime

from backend_roc.utils.error_handle import http_response
from backend_roc.utils.utils import IsAuthenticatedCustom, IsSuperUser, IsTokenValid
from rocapi.serializer.register_serializer import UserSerializer, Countt_user_Serializer, UserListSerializer


class UserAPIView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return http_response(False, serializer.data, status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return http_response(False, serializer.data, status.HTTP_200_OK)

# Countt_user_Serializer

class User_View(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Countt_user_Serializer

    def post(self, request, pk=None):
        serializer = Countt_user_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_date')
            # start_date = '2020-11-07'
            # end_data = '2020-11-25'
            if start_date and end_data is not None:
                date = datetime.strptime(end_data, "%Y-%m-%d").date()
                modified_date = date + timedelta(days=1)
                queryset = User.objects.filter(date_joined__range=[start_date, modified_date])
                serializer = UserSerializer(queryset, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                queryset = User.objects.all()
                serializer = UserListSerializer(queryset, many=True)
                return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
