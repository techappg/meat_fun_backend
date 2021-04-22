# Generated by Django 3.1 on 2020-12-04 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20201203_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.subcategory'),
        ),
    ]
