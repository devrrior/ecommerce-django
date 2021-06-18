from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Article

from .forms import ArticleForm

# Create your views here.


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/new.html'
    success_url = reverse_lazy('articles:create_article')
