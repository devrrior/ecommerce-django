from django.db import models

from core.users.models import CustomUser, SellerUser

import uuid

# Create your models here.


class Article(models.Model):

    class ArticleObjects(models.Model):
        def get_queryset(self):
            return super().get_queryset.filter(status='published')

    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(SellerUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    slug = models.SlugField(blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    # relationship one to many imgs


class Order(models.Model):
    STATUS_CHOICES = (('pending', 'Pending'),
                      ('delivered', 'Deliverded'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        CustomUser, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(
        SellerUser, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=None)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    articles = models.ForeignKey(
        Article, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1, null=True, blank=True)
