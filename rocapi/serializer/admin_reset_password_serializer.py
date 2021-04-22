from rest_framework import serializers

class email_Serializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    OTP = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    # confirm_password = serializers.CharField(required=True)
