# Generated by Django 3.2.4 on 2021-06-16 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_article_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArticleObjects',
        ),
    ]
