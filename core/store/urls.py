from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='store.home_page')
]
