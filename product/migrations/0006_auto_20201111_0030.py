# Generated by Django 3.1 on 2020-11-11 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='header_image',
            name='is_enable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='header_image',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
