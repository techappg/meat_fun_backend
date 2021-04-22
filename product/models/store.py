from django.db import models


class Store(models.Model):
    store_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.CharField(max_length=1000, null=True, blank=True)
    longitude = models.CharField(max_length=1000, null=True, blank=True)
    storeId = models.CharField(max_length=1000, null=True, blank=True)
    is_enable = models.BooleanField(default=True)
    MERCHANT_KEY = models.CharField(max_length=1000, null=True, blank=True)
    MID = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.store_name} ADDRESS {self.address}"