from datetime import datetime

import pytz
from django.utils.timezone import now

from backend_roc.utils.const import MSG_Mobile_Already
from rocapi.models.user_profile import UserProfile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from backend_roc.utils.const import MSG_Email_Already
from rocapi.models import User
from rocapi.models.otp import OTP


def required_and_valid(value):
    if value is None:
        raise serializers.ValidationError('This field is required')
    return True


def required_field():
    return serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def to_representation(self, user):
        user_details = RegisterUserOutputSerializer(user).data
        user_details["profile_image"] = user.userprofile.profile_image.url if user.userprofile.profile_image else ""
        user_details["mobile_no"] = user.userprofile.mobile_no
        # print(f"data : {user_details}")
        # print(f"user : {self.context['request'].user}")
        return user_details

class Countt_user_Serializer(serializers.Serializer):
    user = UserSerializer(many=True, read_only=True)
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)

class RegisterEmailInputSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[required_and_valid, UniqueValidator(queryset=User.objects.all(), message=MSG_Email_Already)])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class adminRegisterEmailInputSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[required_and_valid, UniqueValidator(queryset=User.objects.all(), message=MSG_Email_Already)])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    # otp = serializers.CharField(required=True)


class VerifyEmailInputSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(required=False, default="")
    mobile_no = serializers.CharField(required=False, default="")

    class Meta:
        model = UserProfile
        fields = ('mobile_no', 'profile_image')
    

class RegisterUserOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class EmailOTPSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class SMSOTPSerializer(serializers.Serializer):
    mobile_no = serializers.CharField(required=True)


class VerifyOTPSerializer(serializers.Serializer):
    mobile_no = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class RegisterSMSSerializer(serializers.Serializer):
    mobile_no = serializers.IntegerField(validators=[required_and_valid, UniqueValidator(queryset=UserProfile.objects.all(), message=MSG_Mobile_Already)])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(validators=[required_and_valid, UniqueValidator(queryset=User.objects.all(), message=MSG_Email_Already)])
    otp = serializers.CharField(required=True)


class resetpasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class UserRegisterOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def to_representation(self, user):
        user_details = UserRegisterOutputSerializer(user).data
        user_details["mobile_no"] = user.userprofile.mobile_no
        return user_details
