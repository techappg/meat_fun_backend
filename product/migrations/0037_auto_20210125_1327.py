# Generated by Django 3.1 on 2021-01-25 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_auto_20210125_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='MRP',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]