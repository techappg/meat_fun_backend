from docutils.nodes import status
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_roc.utils.const import OTP_EMAIL_SUBJECT
from rocapi.interface.email_interface import send_email
from rocapi.models.otp import OTP
from rocapi.serializer.admin_reset_password_serializer import email_Serializer
from django.contrib.auth.models import User

class admin_reset_passwordApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = email_Serializer

    def post(self, request, *args, **kwargs):
        serializer = email_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            otp = serializer.data.get("OTP")
            password = serializer.data.get("password")
            # confirm_password = serializer.data.get("confirm_password")
            if password:
                try:
                    opt_user = OTP.objects.get(email=email, otp=otp)
                except OTP.DoesNotExist:
                    opt_user = None

                if opt_user:
                    try:
                        user = User.objects.get(email=email, is_superuser=True)
                        user.set_password(password)
                        user.save()
                        response = {
                            'status': 'success',
                            'code': status.HTTP_200_OK,
                            'message': 'Password updated successfully',
                            'data': []
                        }
                        return Response(response)
                    except:
                        response = {
                            'status': 'error',
                            'code': status.HTTP_400_BAD_REQUEST,
                            'message': 'User Dose Not Exists',
                            'data': []
                        }
                        return Response(response)

                else:
                    response = {
                        'status': 'error',
                        'code': status.HTTP_400_BAD_REQUEST,
                        'message': 'OTP Dose Not Match',
                        'data': []
                    }
                    return Response(response)
            else:
                response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Password Dose Not Match',
                    'data': []
                }
                return Response(response)
