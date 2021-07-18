from django.urls import path
from core.articles.views import ArticleCreateView, ArticleFormView

urlpatterns = [
    # Home page
    path('new', ArticleCreateView.as_view(), name='article.create_article'),
    # Detail artilce
    path('<slug:slug>', ArticleFormView.as_view(),
         name='article.detail_article'),
]
