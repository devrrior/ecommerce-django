from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from core.articles.models import Article, ImageArticle

from core.articles.forms import ArticleForm

# Create your views here.


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/new.html'
    # TODO When the article was created, redirect to the new article
    success_url = reverse_lazy('store.home_page')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        images = self.request.FILES.getlist('images')

        order = 0

        for image in images:
            order += 1
            ImageArticle.objects.create(
                article=article, image=image, article_status=article.status, order=order)

        return super().form_valid(form)
