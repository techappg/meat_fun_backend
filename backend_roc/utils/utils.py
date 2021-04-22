from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser, User
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from backend_roc.settings.base import TESTING
from backend_roc.utils.exceptions import MissingAPIVersion
from rocapi.models.blacklist_jwt_token import BlackListedToken


def get_user_jwt(request):
    user = get_user(request)
    if not isinstance(user, AnonymousUser):
        if user.is_authenticated:
            return user
    try:
        user_jwt = JWTAuthentication().authenticate(request)
        if user_jwt is not None:
            return user_jwt[0]
    except:
        pass
    return user


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        print(f"user: {request.user}")
        if not TESTING:
            u = get_user_jwt(request)
            try:
                request.user = User.objects.get(id=u.id)
            except Exception:
                raise MissingAPIVersion()
        return request.user and request.user.is_authenticated


class IsSuperUser(permissions.BasePermission):
    # message = {"status": "you don't have super user permission"}
    message = {
        'data': [{'error_desc': "you don't have super user permission"}]
    }

    def __init__(self):
        super().__init__()

    def has_permission(self, request, view):
        print(f"user_type : {request.user.is_superuser}")
        return request.user.is_superuser


class IsTokenValid(BasePermission):
    message = {
        'data': [{'error_desc': "token has been expired"}]
    }

    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True
        # print(f"request.auth: {request.auth}")
        token = request.auth
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
