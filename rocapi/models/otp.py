from django.db import models


class OTP(models.Model):
    mobile_no = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200, null=True)
    otp = models.IntegerField(null=True)
    status = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
