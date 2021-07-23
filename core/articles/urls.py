from django.urls import path
from core.articles.views import ArticleCreateView, ArticleFormView

app_name = 'article'
urlpatterns = [
    # Home page
    path('new', ArticleCreateView.as_view(), name='create'),
    # Detail artilce
    path('<slug:slug>', ArticleFormView.as_view(),
         name='show'),
]
