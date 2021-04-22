from django.db import models

class header_image(models.Model):
    image = models.FileField(upload_to='media/')
    default_image = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=100)