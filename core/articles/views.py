from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Article, ImageArticle

from .forms import ArticleForm

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

        for image in images:
            ImageArticle.objects.create(article=article, image=image)

        return super().form_valid(form)
