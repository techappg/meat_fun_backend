from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend_roc.utils.error_handle import http_response
from backend_roc.utils.utils import IsAuthenticatedCustom
from rocapi.models.user_profile import UserProfile
from rocapi.serializer.admin_profile_serializer import adminProfileUpdateSerializer
from rocapi.services.admin_service import AdminService


class adminProfileUpdateApi(mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = adminProfileUpdateSerializer

    def post(self, request):
        serializer = adminProfileUpdateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            user = AdminService.update(self.request.user.id, **validated_data)
            user_details = AdminService.profile_output(user)
            return http_response(True, user_details, status.HTTP_201_CREATED)
        return http_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = adminProfileUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            mobile_no = serializer.data.get('mobile_no')

            user_user = self.request.user
            q = UserProfile.objects.filter(mobile_no=mobile_no)
            if mobile_no is not None:
                if q.exists():
                    return Response("mobile number already exists", status.HTTP_400_BAD_REQUEST)
            if old_password:
                if not user_user.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                if new_password is None:
                    return Response("plz enter new password", status.HTTP_400_BAD_REQUEST)

                if new_password:
                    user = AdminService.update(self.request.user.id, **validated_data)
                    user_details = AdminService.profile_output(user)

                    user_user.set_password(serializer.data.get("new_password"))
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
                user = AdminService.update(self.request.user.id, **validated_data)
                user_details = AdminService.profile_output(user)
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': ' updated successfully',
                    'data': [user_details]
                }
                return Response(response, status.HTTP_201_CREATED)
        return http_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)

