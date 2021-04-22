from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from product.models.products import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_item_price(self):
        price = float(self.item.price)
        return self.quantity * price

    def get_discount(self):
        if self.item.discount:
            dis = self.item.discount / 100
            p = float(self.item.price) * float(dis)
            q = self.quantity * p
            return q

    def get_final_amount(self):
        return float(self.get_total_item_price())

