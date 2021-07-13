from django.urls import path
from core.store.views import ArticleListView

urlpatterns = [
    # Home page
    path('', ArticleListView.as_view(), name='store.home_page')
]
