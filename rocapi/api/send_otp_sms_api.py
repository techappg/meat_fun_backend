import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.const import FAILED_OTP_SEND, OTP_TEMPLATE
from rocapi.interface.text_sms_interface import send_text
from rocapi.models.otp import OTP
from rocapi.serializer.register_serializer import SMSOTPSerializer


class SendOTPSMSApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = SMSOTPSerializer

    def post(self, request):
        serializer = SMSOTPSerializer(data=request.data)
        final_response = dict()
        if serializer.is_valid(raise_exception=True):
            mobile_no = serializer.data.get("mobile_no")
            otp_number = random.randint(1000, 9999)
            final_msg = OTP_TEMPLATE.replace("<OTP>", str(otp_number))
            otp, created = OTP.objects.get_or_create(mobile_no=mobile_no)
            otp.otp = otp_number
            resp_status = send_text(mobile_no, final_msg)
            if resp_status == "success":
                final_response['error'] = False
                data = {
                    "otp": otp_number,
                    "mobile_no": mobile_no,
                    "user_status": User.objects.filter(username=mobile_no).exists()
                }
            else:
                final_response['error'] = True
                data = {
                    "error_desc": FAILED_OTP_SEND,
                    "mobile_no": mobile_no
                }
            otp.status = resp_status
            otp.save()

            final_response['data'] = data
            return Response(final_response, status.HTTP_200_OK)
