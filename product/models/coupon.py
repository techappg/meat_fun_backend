from django.db import models
from django.contrib.auth.models import User

from product.models.Subcategory import Subcategory
from product.models.booklet import Booklet
from product.models.category import Category
from product.models.products import Product
from product.models.store import Store

STATUS_CHOICES = (
    ("All User", "All User"),
    ("First user", "First user"),)
    # ("successfully delivered", "successfully delivered"), )

class Coupon(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    coupon_code = models.CharField(max_length=15)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)
    number_of_coupon = models.PositiveIntegerField(default=0, blank=True)
    coupon_for = models.CharField(max_length=50, choices=STATUS_CHOICES)
    product_master_key = models.CharField(max_length=100, blank=True, null=True)
    minimum_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    discount_percent = models.PositiveIntegerField(default=0, blank=True, null=True)
    discount_amount = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.coupon_code


