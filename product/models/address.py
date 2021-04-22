from django.db import models
from django.contrib.auth.models import User

ADDRESS_CHOICES = (
    ('Billing', 'Billing'),
    ('Shipping', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=10, choices=ADDRESS_CHOICES)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    apartment_address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=13, null=True)


    def __str__(self):
        return self.user.username

