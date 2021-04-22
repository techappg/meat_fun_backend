from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from backend_roc.utils.const import OTP_EXPIRED_MSG
from backend_roc.utils.error_handle import http_response
from rocapi.models.otp import OTP
from rocapi.serializer.register_serializer import VerifyOTPSerializer
from datetime import date, timezone, timedelta, datetime
from django.utils import timezone


class VerifyMobileOnlyOtpLoginApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_no = serializer.data.get("mobile_no")
            otp = serializer.data.get("otp")
            try:
                opt_user = OTP.objects.get(mobile_no=mobile_no, otp=otp)

                date = opt_user.updated_at
                now_plus_10 = date + timedelta(minutes=5)
                datetoday = timezone.now()

                if now_plus_10 < datetoday:
                    return http_response(True, OTP_EXPIRED_MSG, status.HTTP_201_CREATED)
                else:
                    return http_response(False, "OTP successfully matched", status.HTTP_201_CREATED)
            except:
                return http_response(True, "your OTP dose not matched", status.HTTP_201_CREATED)

