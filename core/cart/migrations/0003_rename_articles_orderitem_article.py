# Generated by Django 3.2.4 on 2021-07-16 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='articles',
            new_name='article',
        ),
    ]
