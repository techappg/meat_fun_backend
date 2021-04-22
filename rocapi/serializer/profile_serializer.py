from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from backend_roc.utils.const import MSG_Mobile_Already
from rocapi.models.user_profile import UserProfile


class ProfileUpdateSerializer(serializers.Serializer):
    profile_image = serializers.FileField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    mobile_no = serializers.CharField(required=False, validators=[ UniqueValidator(queryset=UserProfile.objects.all(), message=MSG_Mobile_Already)])
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)
    confirm_password = serializers.CharField(required=False)

    def get_profile_image(self, obj):
        # if obj.profile_image:
            # return self.context["request"].build_absolute_uri(obj.profile_image.url)

        print(self.context["request"].build_absolute_uri(obj.profile_image.url))
        return self.context["request"].build_absolute_uri(obj.profile_image.url)