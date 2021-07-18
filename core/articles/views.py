# TODO check if the article's stock > 0 display
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from core.articles.models import Article, ImageArticle
from core.cart.models import Order, OrderItem

from core.articles.forms import CreateArticleForm, AddToCartForm


class ArticleFormView(FormView):
    template_name = 'articles/article_detail.html'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('store.home_page')

    def form_valid(self, form):
        # TODO check if order_item.quantity <= stocke

        customer = self.request.user
        order = Order.objects.get_or_create(
            customer=customer, ordered=False)[0]
        article = self.get_object()
        item_filter = order.orderitem_set.filter(article_id=article.id)

        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
            item.save()
            messages.success(self.request, 'The item was created in the cart')
        else:
            new_item = form.save(commit=False)
            new_item.article = article
            new_item.order = order
            new_item.quantity = int(form.cleaned_data['quantity'])
            new_item.save()
            messages.success(self.request, 'The item was created in the cart')

        return super(ArticleFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleFormView, self).get_context_data(**kwargs)
        context['article'] = self.get_object()
        context['article'].images = ImageArticle.objects.filter(
            article_id=context['article'].id).order_by('order')

        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = CreateArticleForm
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
