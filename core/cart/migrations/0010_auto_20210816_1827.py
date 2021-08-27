# Generated by Django 3.2.5 on 2021-08-16 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_alter_imagearticle_article'),
        ('cart', '0009_auto_20210816_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='articles.article'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='cart.order'),
        ),
    ]