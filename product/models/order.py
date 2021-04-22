from django.db import models
from django.contrib.auth.models import User
from product.models.address import Address
from product.models.cart import Cart
from product.models.coupon import Coupon

STATUS_CHOICES = (
    ("Inprocess", "Inprocess"),
    ("processed", "processed"),
    ("out for delivery", "out for delivery"),
    ("successfully delivered", "successfully delivered"),("order cancel", "order cancel"), )

PAYMENT_MODE_CHOICES = (
    ("COD", "COD"),
    ("ONLINE PAY", "ONLINE PAY"), )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    order_status = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100)

    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Inprocess')
    delivery_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    mobile_num = models.CharField(max_length=13, null=True, blank=True)
    choice = models.CharField(max_length=100, null=True, blank=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES, default='ONLINE PAY')
    store_id = models.IntegerField(null=True, blank=True)
    txnId = models.CharField(max_length=100, null=True, blank=True)
    bankTxnId = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.user.username} ORDER ID {self.order_id}"

    def get_total(self):
        totel = 0.0
        for order_item in self.items.all():
            totel += order_item.get_final_amount()
        if self.coupon:
            if self.coupon.discount_percent:
                dis = float(self.coupon.discount_percent) / 100
                totel_dis = dis * totel
                totel -= totel_dis
                return totel
            else:
                tot_dis = self.coupon.discount_amount
                totel -= tot_dis
                print(totel)
                return totel
        return totel

    def address(self):
        return f"{self.shipping_address.street_address} {self.shipping_address.apartment_address} {self.shipping_address.city} {self.shipping_address.zip}"


class Transaction(models.Model):
    razorpay_payment_id = models.CharField(max_length=1000)
    razorpay_order_id = models.CharField(max_length=1000)
    razorpay_signature = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
