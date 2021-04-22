import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.const import OTP_EMAIL_SUBJECT, OTP_EMAIL_TEMPLATE, \
    FAILED_OTP_SEND
from rocapi.interface.email_interface import send_email
from rocapi.models.otp import OTP
from rocapi.serializer.register_serializer import EmailOTPSerializer


class SendOTPEmailApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = EmailOTPSerializer

    def post(self, request):
        serializer = EmailOTPSerializer(data=request.data)
        final_response = dict()
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            otp_number = random.randint(1000, 9999)
            final_msg = OTP_EMAIL_TEMPLATE.replace("<OTP>", str(otp_number))
            otp, created = OTP.objects.get_or_create(email=email)
            otp.otp = otp_number
            resp_status = send_email(final_msg, OTP_EMAIL_SUBJECT, email)

            if resp_status == "success":
                final_response['error'] = False
                data = {
                    "otp": otp_number,
                    "mobile_no": email,
                    "user_status": User.objects.filter(username=email).exists()
                }
            else:
                final_response['error'] = True
                data = {
                    "error_desc": FAILED_OTP_SEND,
                    "mobile_no": email
                }
            otp.status = resp_status
            otp.save()

            final_response['data'] = data
            return Response(final_response, status.HTTP_200_OK)
