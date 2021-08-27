# TODO check if the article's stock > 0 display
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import FormView
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
        return reverse_lazy('cart:summary')

    def form_valid(self, form):
        # TODO improve method

        customer_id = self.request.user.id
        article_id = self.kwargs['slug'][-36:]
        quantity = int(form.cleaned_data['quantity'])
        order, order_created = Order.objects.get_or_create(
            customer_id=customer_id, ordered=False)

        order_item, order_item_created = OrderItem.objects.select_related(
            'article'
        ).get_or_create(
            article_id=article_id, order_id=order.id,
        )

        article_stock = order_item.article.stock
        enough_stock_of_article = article_stock >= order_item.quantity + quantity

        if order_item_created and enough_stock_of_article:
            order_item.quantity = quantity
            order_item.save()
            messages.success(self.request, 'The item was created in the cart')
        elif not order_item_created and enough_stock_of_article:
            order_item.quantity += quantity
            order_item.save()
            messages.success(self.request, 'The item was created in the cart')
        else:
            order_item.delete()
            messages.warning(self.request, 'There is not enough stock')

        return super(ArticleFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleFormView, self).get_context_data(**kwargs)
        article = Article.objects.prefetch_related(
            Prefetch(
                'imagearticles',
                queryset=ImageArticle.objects.filter(
                    article__slug=self.kwargs['slug']
                ).order_by('order'),
                to_attr='get_images',
            )
        ).get(slug=self.kwargs['slug'])
        context['article'] = article
        context['article'].images = article.get_images

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
