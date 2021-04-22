from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend_roc.utils.const import LOGOUT_MSG
from backend_roc.utils.error_handle import http_response
from backend_roc.utils.utils import IsAuthenticatedCustom, IsTokenValid
from rocapi.services.admin_service import AdminService


class LogoutApi(APIView):
    permission_classes = [IsAuthenticatedCustom, IsTokenValid]

    def post(self, request):
        token = request.auth
        user = request.user
        AdminService.logout(user, token)
        return http_response(True, LOGOUT_MSG, status.HTTP_200_OK)
