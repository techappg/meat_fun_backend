from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type
from backend_roc.utils.const import OTP_NOT_MATCH_MSG
from backend_roc.utils.error_handle import http_response
from rocapi.models.otp import OTP
from rocapi.serializer.register_serializer import adminRegisterEmailInputSerializer, RegisterUserOutputSerializer
from rocapi.services.admin_service import AdminService


class adminVerifyEmailOtpRegisterApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = adminRegisterEmailInputSerializer

    def post(self, request):
        data = request.data
        serializer = adminRegisterEmailInputSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            first_name = serializer.data.get("first_name")
            last_name = serializer.data.get("last_name")
            if serializer:
                user = AdminService.create_user(username=email,
                                               email=email,
                                               first_name=first_name,
                                               last_name=last_name,
                                               )
                user_details = AdminService.profile_output(user)
                token = RefreshToken.for_user(user)
                jwt_token = {
                    'access': text_type(token.access_token),
                    'refresh': text_type(token),
                }
                response = {
                    'jwt_token': jwt_token,
                    'user_details': user_details
                }
                return http_response(False, response, status.HTTP_201_CREATED)
            else:
                return http_response(True, OTP_NOT_MATCH_MSG, status.HTTP_201_CREATED)
