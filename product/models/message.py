from django.db import models

SMS_CHOICES = (
    ("franchisses", "franchisses"),

)

class SMS(models.Model):
    message = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sms_type = models.CharField(max_length=60, choices=SMS_CHOICES)

    def __str__(self):
        return self.message
