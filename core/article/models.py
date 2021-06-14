from django.db import models

# Create your models here.


class Article(models.Model):

    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'), )

    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    slug = models.SlugField(blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    # relationship one to many imgs
    # realtionship one to many opinions
    # relationship one to many questions
