# Generated by Django 3.2.4 on 2021-06-18 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_address_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='seller',
            field=models.BooleanField(default=False),
        ),
    ]
