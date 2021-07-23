from django.urls import path
from core.store.views import ArticleListView

app_name = 'store'
urlpatterns = [
    # Home page
    path('', ArticleListView.as_view(), name='index')
]
