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
        images_article = ImageArticle.imagearticleobjects.all()
        for article in context['object_list']:
            for image_article in images_article:
                if article.id == image_article.article_id:
                    article.image_article = image_article

        # print('imagen', context['object_list'][0].image_article.url)
        return context
