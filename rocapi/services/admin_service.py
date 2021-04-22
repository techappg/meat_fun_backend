from django.contrib.auth.models import User

from rocapi.models.blacklist_jwt_token import BlackListedToken
from rocapi.models.user_profile import UserProfile
from rocapi.serializer.register_serializer import RegisterUserOutputSerializer


class AdminService(object):

    @staticmethod
    def create_user(username=None, first_name=None, last_name=None, mobile_no=None, email=None):

        user = User.objects.create(username=username)
        if email:
            user.email = email
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.mobile_no = mobile_no
        user_profile.user_type = 'admin'
        user_profile.save()
        return user

    @staticmethod
    def get(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def update(user_id, **fields):
        user = AdminService.get(user_id)
        user.first_name = fields.get('first_name', user.first_name)
        user.last_name = fields.get('last_name', user.last_name)
        if fields.get('password'):
            user.set_password(fields.get('password'))
        user.save()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.mobile_no = fields.get('mobile_no', user_profile.mobile_no)
        # user_profile.profile_image = fields.get('profile_image', user_profile.profile_image if user_profile.profile_image else "profile/avatar.png")
        user_profile.save()

        return user

    @staticmethod
    def profile_output(user):
        user_details = RegisterUserOutputSerializer(user).data
        # user_details["profile_image"] = user.userprofile.profile_image.url if user.userprofile.profile_image else ""
        user_details["mobile_no"] = user.userprofile.mobile_no
        return user_details

    @staticmethod
    def logout(user, token):
        blacklist, created = BlackListedToken.objects.get_or_create(user=user)
        blacklist.token = token
        return blacklist.save()
