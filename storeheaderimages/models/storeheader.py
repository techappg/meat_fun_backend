from django.db import models

from product.models.store import Store


class Storeheader(models.Model):
    image = models.FileField(upload_to='media/')
    default_image = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,  null=True, blank=True)
