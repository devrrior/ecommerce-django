from django.urls import path
from core.articles.views import ArticleCreateView

urlpatterns = [
    # Home page
    path('new', ArticleCreateView.as_view(), name='article.create_article')
]
