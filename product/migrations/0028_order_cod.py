# Generated by Django 3.1 on 2020-12-09 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_product_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='COD',
            field=models.BooleanField(default=False),
        ),
    ]
