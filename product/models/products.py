from django.db import models
from product.models.Subcategory import Subcategory
from product.models.category import Category
from product.models.store import Store


class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    MRP = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0,  null=True, blank=True)
    quantity_type = models.CharField(max_length=100)
    discount = models.PositiveIntegerField(default=0,  null=True, blank=True)
    tax_CGST = models.CharField(max_length=100, null=True, blank=True)
    tax_SGST = models.CharField(max_length=100, null=True, blank=True)
    Enable = models.BooleanField(default=True)
    keyword = models.CharField(max_length=1000,  null=True, blank=True)
    default_image = models.FileField(upload_to='media/', null=False, blank=False)
    productUsage = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)
    master_key = models.CharField(max_length=10)
    product_code = models.CharField(max_length=10)
    seo_title = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.FileField(upload_to='media/')
