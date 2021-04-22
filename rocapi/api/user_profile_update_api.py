from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend_roc.utils.error_handle import http_response
from backend_roc.utils.utils import IsAuthenticatedCustom
from rocapi.serializer.profile_serializer import ProfileUpdateSerializer
from rocapi.services.user_service import UserService


class UserProfileUpdateApi(mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileUpdateSerializer

    def post(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            user = UserService.update(self.request.user.id, **validated_data)
            user_details = UserService.profile_output(user)
            return http_response(True, user_details, status.HTTP_201_CREATED)
        return http_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_password')

            user_user = self.request.user

            if old_password:
                if not user_user.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                if new_password is None:
                    return Response("plz enter new password", status.HTTP_400_BAD_REQUEST)
                if confirm_password is None:
                    return Response("plz enter confirm password", status.HTTP_400_BAD_REQUEST)

                if new_password == confirm_password:
                    user = UserService.update(self.request.user.id, **validated_data)
                    user_details = UserService.profile_output(user)

                    user_user.set_password(serializer.data.get("confirm_password"))
                    user_user.save()
                    response = {
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'Password updated successfully',
                        'data': [user_details]
                    }
                    return Response(response)
                else:
                    response = {
                        'status': 'error',
                        'code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Password Dose not Match',
                        'data': []
                    }
                    return Response(response)
            else:
                user = UserService.update(self.request.user.id, **validated_data)
                user_details = UserService.profile_output(user)
                return Response(user_details, status.HTTP_201_CREATED)
        return http_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)





