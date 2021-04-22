from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from product.models.Subcategory import Subcategory
from product.models.category import Category
from product.models.order import Order
from product.models.products import Product
from product.models.store import Store
import requests


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # product = Product.objects.get()
        order = Order.objects.filter().count()
        user = User.objects.get(id=1)
        print(order)
        c = 720
        i = 0
        while i <= c:
            i += 1
            order = Order.objects.create(user=user, amount='100')

        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)