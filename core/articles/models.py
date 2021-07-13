from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from core.users.models import CustomUser

import uuid

# Create your models here.


class Article(models.Model):

    class ArticleObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    slug = models.SlugField(blank=True, unique=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    articleobjects = ArticleObjects()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)

    @staticmethod
    def set_slug(sender, instance, *args, **kwargs):
        if instance.slug:
            return
        instance.slug = slugify('{}-{}'.format(instance.title, instance.id))


pre_save.connect(Article.set_slug, sender=Article)


class ImageArticle(models.Model):

    class ImageArticleObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/article/",)
    article_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    imagearticleobjects = ImageArticleObjects()

    def __str__(self):
        return f'{self.article.title}-{self.id}'

    class Meta:
        ordering = ('-created_at',)


class Order(models.Model):
    STATUS_CHOICES = (('pending', 'Pending'),
                      ('delivered', 'Deliverded'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        CustomUser, null=True, on_delete=models.SET_NULL)
    seller_if = models.UUIDField(default=1)
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
