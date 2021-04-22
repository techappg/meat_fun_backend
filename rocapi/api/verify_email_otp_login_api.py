from datetime import date, timezone, timedelta, datetime
from django.utils import timezone

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type

from backend_roc.utils.const import OTP_NOT_MATCH_MSG, USER_NOT_EXIST_MSG, OTP_EXPIRED_MSG
from backend_roc.utils.error_handle import http_response
from rocapi.models.otp import OTP
from rocapi.serializer.register_serializer import VerifyEmailInputSerializer, RegisterUserOutputSerializer
from rocapi.services.user_service import UserService


class VerifyEmailOtpLoginApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = VerifyEmailInputSerializer

    def post(self, request):
        serializer = VerifyEmailInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")
            print(f"{email} # {otp}")
            try:
                opt_user = OTP.objects.get(email=email, otp=otp)

                date = opt_user.updated_at
                now_plus_10 = date + timedelta(minutes=5)
                datetoday = timezone.now()
                print("plus 10 ", now_plus_10)
                print(datetoday)

                if now_plus_10 < datetoday:
                    return http_response(True, OTP_EXPIRED_MSG, status.HTTP_201_CREATED)

            except OTP.DoesNotExist:
                opt_user = None
            # print(f"opt_user: {opt_user}")
            if opt_user:
                try:
                    # user = User.objects.get(username=email)
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = None
                if user is None:
                    return http_response(True, USER_NOT_EXIST_MSG, status.HTTP_201_CREATED)

                user_details = UserService.profile_output(user)
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
