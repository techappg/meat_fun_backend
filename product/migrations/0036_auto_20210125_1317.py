# Generated by Django 3.1 on 2021-01-25 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_auto_20210119_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tax_CGST',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='tax_SGST',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]