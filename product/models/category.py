from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.FileField(upload_to='media/', null=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=True)
    meta_title = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category_like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username



