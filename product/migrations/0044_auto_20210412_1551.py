# Generated by Django 3.1 on 2021-04-12 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_auto_20210406_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
