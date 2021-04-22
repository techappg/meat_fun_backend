from rest_framework import status, generics
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from product.models.booklet import Booklet
from product.serializer.booklet_serializer import Booklet_Serializer


class Booklet_View(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = Booklet_Serializer
    queryset = Booklet.objects.all()

class get_Booklet_View(ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = Booklet.objects.values_list('perfix', flat=True).distinct()
        final_response = dict()
        data = {
            "perfix": queryset,
        }
        final_response['data'] = data
        return Response(final_response, status.HTTP_200_OK)

class delete_Booklet_View(DestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, perfix=None):
        queryset = Booklet.objects.filter(perfix=perfix)
        if queryset.exists():
            queryset.delete()
            return Response("Successfully deleted", status.HTTP_200_OK)
        else:
            return Response("Perfix Dose Not Exists", status.HTTP_400_BAD_REQUEST)

