# Generated by Django 3.2.4 on 2021-07-18 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_order_seller_if'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ordered',
        ),
    ]
