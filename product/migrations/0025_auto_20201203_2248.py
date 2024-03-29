# Generated by Django 3.1 on 2020-12-04 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20201203_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount_amount',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount_percent',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='minimum_amount',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='product_master_key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
