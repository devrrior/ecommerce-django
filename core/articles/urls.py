from django.urls import path
from core.articles.views import ArticleCreateView, ArticleDetailView

urlpatterns = [
    # Home page
    path('new', ArticleCreateView.as_view(), name='article.create_article'),
    # Detail artilce
    path('<slug:slug>', ArticleDetailView.as_view(),
         name='article.detail_article'),
]
