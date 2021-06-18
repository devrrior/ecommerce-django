from django.contrib import admin
from core.articles.models import *

# Register your models here.
admin.site.register(Article)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ImageArticle)
