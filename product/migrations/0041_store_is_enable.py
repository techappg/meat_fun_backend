# Generated by Django 3.1 on 2021-02-10 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_auto_20210127_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_enable',
            field=models.BooleanField(default=True),
        ),
    ]