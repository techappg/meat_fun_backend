import coreapi
import coreschema
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type
from backend_roc.utils.error_handle import http_response
from rocapi.serializer.register_serializer import LoginSerializer
from rocapi.services.admin_service import AdminService


class adminLoginView(APIView):
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="username",
                required=True,
                location="form",
                schema=coreschema.String(description="Username is required"),
            ),
            coreapi.Field(
                name="password",
                required=True,
                location="form",
                schema=coreschema.String(description="Password is required"),
            ),
        ]
    )
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            print(f"{username}#{password}")
            user_auth = authenticate(username=username, password=password)
            if not user_auth:
                return http_response(True, 'Invalid Credentials', status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=user_auth)
            token = RefreshToken.for_user(user)
            jwt_token = {
                'access': text_type(token.access_token),
                'refresh': text_type(token),
            }
            response = {
                'jwt_token': jwt_token,
                'user_details': AdminService.profile_output(user)
            }
            return http_response(False, response, status.HTTP_201_CREATED)

