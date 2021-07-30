# TODO check if the article's stock > 0 display
from core.cart.utils import verify_stock
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from core.articles.models import Article, ImageArticle
from core.cart.models import Order

from core.articles.forms import CreateArticleForm, AddToCartForm


class ArticleFormView(FormView):
    template_name = 'articles/article_detail.html'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('cart:summary')

    def form_valid(self, form):
        # TODO check if order_item.quantity <= stocke

        customer = self.request.user
        order = Order.objects.get_or_create(customer=customer, ordered=False)[0]
        article = self.get_object()
        item_filter = order.orderitem_set.filter(article_id=article.id)
        quantity = int(form.cleaned_data['quantity'])

        if item_filter.exists():
            item = item_filter.first()
            if verify_stock(article.stock, quantity):
                item.quantity += quantity
                item.save()
                messages.success(self.request, 'The item was created in the cart')
            else:
                messages.warning(self.request, 'There is not enough stock')

        else:
            new_item = form.save(commit=False)
            new_item.article = article
            new_item.order = order
            if article.stock >= quantity:
                new_item.quantity = int(form.cleaned_data['quantity'])
                new_item.save()
                messages.success(self.request, 'The item was created in the cart')
            else:
                messages.warning(self.request, 'There is not enough stock')

        return super(ArticleFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleFormView, self).get_context_data(**kwargs)
        context['article'] = self.get_object()
        context['article'].images = ImageArticle.objects.filter(
            article_id=context['article'].id
        ).order_by('order')

        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = CreateArticleForm
    # TODO When the article was created, redirect to the new article
    success_url = reverse_lazy('article:create')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        images = self.request.FILES.getlist('images')

        order = 0

        for image in images:
            order += 1
            ImageArticle.objects.create(
                article=article, image=image, article_status=article.status, order=order
            )

        return super(ArticleCreateView, self).form_valid(form)
