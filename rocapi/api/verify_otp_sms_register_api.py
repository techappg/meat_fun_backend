from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type
from backend_roc.utils.const import OTP_NOT_MATCH_MSG, OTP_EXPIRED_MSG
from backend_roc.utils.error_handle import http_response
from rocapi.models.otp import OTP
from rocapi.serializer.register_serializer import RegisterSMSSerializer, RegisterUserOutputSerializer

from rocapi.services.user_service import UserService
from datetime import date, timezone, timedelta, datetime
from django.utils import timezone


class VerifyOtpSMSRegisterApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSMSSerializer

    def post(self, request):
        serializer = RegisterSMSSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_no = serializer.data.get("mobile_no")
            first_name = serializer.data.get("first_name")
            last_name = serializer.data.get("last_name")
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")

            try:
                opt_user = OTP.objects.get(mobile_no=mobile_no, otp=otp)
                date = opt_user.updated_at
                now_plus_10 = date + timedelta(minutes=5)
                datetoday = timezone.now()

                if now_plus_10 < datetoday:
                    return http_response(True, OTP_EXPIRED_MSG, status.HTTP_201_CREATED)

            except OTP.DoesNotExist:
                opt_user = None

            if opt_user:
                user = UserService.create_user(username=mobile_no,
                                               mobile_no=mobile_no,
                                               first_name=first_name,
                                               last_name=last_name,
                                               email=email
                                               )
                token = RefreshToken.for_user(user)
                jwt_token = {
                    'access': text_type(token.access_token),
                    'refresh': text_type(token),
                }
                user.refresh_from_db()
                user_details = UserService.profile_output(user)
                response = {
                    'jwt_token': jwt_token,
                    'user_details': user_details
                }
                return http_response(False, response, status.HTTP_201_CREATED)
            else:
                return http_response(True, {"message": OTP_NOT_MATCH_MSG}, status.HTTP_201_CREATED)
