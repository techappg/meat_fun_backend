from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from product.models.order import Order


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        today_date = date.today()
        orders = Order.objects.filter(order_status=True, updated_at__gte=today_date, status__range=["out for delivery", "processed" ])
        for order in orders:

            if order.status == 'out for delivery':
                order_status_update_time = order.updated_at + timedelta(minutes=30)
                order_time = timezone.now()
                if order_status_update_time <= order_time:
                    order.status = 'successfully delivered'
                    order.save()

            if order.status == 'processed':
                order_status_update_time = order.updated_at + timedelta(minutes=30)
                order_time = timezone.now()
                if order_status_update_time <= order_time:
                    order.status = 'successfully delivered'
                    order.save()

        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)