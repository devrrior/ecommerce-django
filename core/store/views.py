from django.shortcuts import render
from django.views.generic.list import ListView

from core.articles.models import Article, ImageArticle

# Create your views here.


class ArticleListView(ListView):
    model = Article
    paginate_by = 30
    template_name = 'store/index.html'

    # For show just published articles
    def get_queryset(self):
        return Article.articleobjects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_article'] = ImageArticle.imagearticleobjects.all()
        print(context)
        return context
