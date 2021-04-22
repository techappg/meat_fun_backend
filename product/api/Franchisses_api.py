import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.const import FRANCHISEES_TEMPLATE, FRANCHISSES_SEND_FAILED
from product.models.franchisses import Franchisses
from product.models.message import SMS
from product.serializer.franchisses_serializer import franchissesSerializer
from rocapi.interface.text_sms_interface import send_text


class franchissesApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = franchissesSerializer

    def post(self, request):
        serializer = franchissesSerializer(data=request.data)
        final_response = dict()
        if serializer.is_valid(raise_exception=True):
            name = serializer.data.get("name")
            city = serializer.data.get("city")
            mobile_no = serializer.data.get("mobile_no")
            message = serializer.data.get("message")
            f_msg = SMS.objects.filter(sms_type='franchisses').first()
            final_msg = FRANCHISEES_TEMPLATE.replace("<name>", str(f_msg))
            Franc = Franchisses.objects.create(name=name,
                                               city=city,
                                               message=message,
                                               mobile_no=mobile_no, )
            resp_status = send_text(mobile_no, final_msg)
            if resp_status == "success":
                final_response['error'] = False
                data = {
                    "name": name,
                    "city":city,
                    "message":message,
                    "mobile_no":mobile_no
                }
            else:
                final_response['error'] = True
                data = {
                    "error_desc": FRANCHISSES_SEND_FAILED,
                }
            Franc.save()
            final_response['data'] = data
            return Response(final_response, status.HTTP_200_OK)

    def get(self, request):
        queryset = Franchisses.objects.all()
        serializer = franchissesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class franchissesGet(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = franchissesSerializer

    def get(self, request, pk):
        queryset = Franchisses.objects.get(id=pk)
        serializer = franchissesSerializer(queryset)
        return Response(serializer.data)

    # def patch(self, request, pk):
    #     queryset = Menu.objects.get(id=pk)
    #     serializer = MenuPatchSerializer(queryset, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            queryset = Franchisses.objects.get(id=pk)
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("id dose not exists", status=status.HTTP_400_BAD_REQUEST)