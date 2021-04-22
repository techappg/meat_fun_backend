# Generated by Django 3.1 on 2020-11-27 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_us',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.PositiveIntegerField(max_length=13)),
                ('contact', models.CharField(max_length=1000)),
            ],
        ),
    ]