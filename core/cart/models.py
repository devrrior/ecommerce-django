from django.db import models
from django.db.models.fields.related import ForeignKey

from core.cart.validators import validate_positive

from core.articles.models import Article
from core.users.models import CustomUser

import uuid


class DiscountCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(unique=True, max_length=6)
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


class Order(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        CustomUser, null=True, on_delete=models.SET_NULL)
    ordered = models.BooleanField(default=False)
    total = models.FloatField(default=0, validators=[validate_positive])
    discount_code = models.ForeignKey(
        DiscountCode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(
        Article, on_delete=models.SET_NULL, null=True, related_name='articles'
    )
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, related_name='orders'
    )
    # cover_image = ForeignKey()
    quantity = models.IntegerField(default=1, null=True, blank=True)
