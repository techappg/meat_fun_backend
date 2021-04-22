# Generated by Django 3.1 on 2021-04-06 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0042_auto_20210226_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seo_title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Inprocess', 'Inprocess'), ('processed', 'processed'), ('out for delivery', 'out for delivery'), ('successfully delivered', 'successfully delivered'), ('order cancel', 'order cancel')], default='Inprocess', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='keyword',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]