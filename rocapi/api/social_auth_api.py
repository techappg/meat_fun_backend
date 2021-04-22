from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_social_oauth2.views import ConvertTokenView
from oauth2_provider.models import AccessToken
from rest_framework.views import APIView
import json
import coreapi
import coreschema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type
from rest_framework.schemas import ManualSchema
from backend_roc.utils.error_handle import http_response
from rocapi.serializer.register_serializer import RegisterUserOutputSerializer
from rocapi.services.user_service import UserService


class SocialConvertTokenSerializer(serializers.Serializer):
    grant_type = serializers.CharField(required=True, help_text='convert_token')
    client_id = serializers.CharField(required=True)
    client_secret = serializers.CharField(required=True)
    backend = serializers.CharField(required=True)
    token = serializers.CharField(required=True)


class SocialConvertTokenView(ConvertTokenView, APIView):
    permission_classes = (AllowAny,)
    serializer_class = SocialConvertTokenSerializer
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                name="grant_type",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='convert_token',

            ),
            coreapi.Field(
                "client_id",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='OAuth Application Client ID'
            ),
            coreapi.Field(
                "client_secret",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='OAuth Application Client Secret',
            ),
            coreapi.Field(
                "backend",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='facebook',
            ),
            coreapi.Field(
                "token",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='Facebook Auth Token',
            ),
        ],
        description='Create Account from Facebook Auth Token',
        encoding='application/json'
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        url, headers, body, status_code = self.create_token_response(request._request)

        if 'error' in body:
            return Response(json.loads(body), status=status.HTTP_400_BAD_REQUEST)

        try:
            oauth_token = AccessToken.objects.get(token=json.loads(body).get('access_token'))
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        print("OAuth token user : ", oauth_token.user)

        token = RefreshToken.for_user(oauth_token.user)
        jwt_token = {
            'access': text_type(token.access_token),
            'refresh': text_type(token),
        }
        user_details = UserService.profile_output(oauth_token.user)
        response = {
            'jwt_token': jwt_token,
            'user_details': user_details
        }
        return http_response(False, response, status.HTTP_201_CREATED)
