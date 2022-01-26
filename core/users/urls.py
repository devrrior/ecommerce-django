from django.urls import path
from .views import OrderListView

app_name = 'users'

urlpatterns = [
    path('my_purchases/', OrderListView.as_view(), name='my_purchases'),
]
