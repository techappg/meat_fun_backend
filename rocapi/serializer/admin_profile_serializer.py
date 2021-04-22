from rest_framework import serializers


class adminProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    mobile_no = serializers.CharField(required=False)
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)
    # confirm_password = serializers.CharField(required=False)

