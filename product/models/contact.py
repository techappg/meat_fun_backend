from django.db import models

class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=13)
    contact = models.CharField(max_length=1000)
    title = models.CharField(max_length=100, null=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class Career(models.Model):
    cv = models.FileField(upload_to='media/', null=False, blank=False)
