from django.db import models
from django.contrib.auth.models import User

class Booklet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booklet_no = models.CharField(max_length=100)
    perfix = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.perfix