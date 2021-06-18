from django.urls import path
from .views import ArticleCreateView

urlpatterns = [
    # Home page
    path('new', ArticleCreateView.as_view(), name='create_article')
]
