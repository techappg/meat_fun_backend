from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class Is_admin(permissions.BasePermission):

    def has_permission(self, request, view):
        # if request.method in SAFE_METHODS:
        #     return request.method in SAFE_METHODS

        user_obj = request.user.is_superuser == True
        # return request.user and user_obj
        return bool(
            request.method in SAFE_METHODS or
            request.user and user_obj
        )
