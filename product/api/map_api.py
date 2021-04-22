from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.google_map import G_MAP
from product.interface.google_send_data import send_google_text
from product.serializer.google_map_serializer import map_serializer

# o_lat = 30.741929
# o_long = 76.672851
# d_lat = 30.7046486
# d_lat = 76.71787259999999
import json
class g_map_View(GenericAPIView):

    permission_classes = [AllowAny, ]
    serializer_class = map_serializer

    def post(self, request):
        serializer = map_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            origins_lat = serializer.data.get('origins_lat')
            origins_long = serializer.data.get('origins_long')
            dest_lat = serializer.data.get('dest_lat')
            dest_long = serializer.data.get('dest_long')
            text_url = send_google_text(origins_lat, origins_long, dest_lat, dest_long)

            ll = ""
            for tt in text_url:
                new_str = tt.decode('utf-8')
                ll += new_str

            y = json.loads(ll)
            data = y["rows"]

            return Response(data, status.HTTP_200_OK)
