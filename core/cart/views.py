from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages

from core.cart.models import Order, OrderItem
from core.articles.models import Article

from core.cart.utils import verify_stock


class CartView(TemplateView):
    template_name = 'cart/cart.html'

    # TODO conseguir solo los datos que quiere
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['order_items'] = []
        articles = Article.objects.all().only()

        try:
            order = Order.objects.get(customer_id=self.request.user.id,
                                      ordered=False)
        except ObjectDoesNotExist:
            context['empty'] = True
            return context

        order_items = order.orderitem_set.all().order_by('-id')
        order_total = 0

        i = 1
        for order_item in order_items:

            article = articles.filter(id=order_item.article_id).first()
            article_image = article.imagearticle_set.get(order=1).image
            data = {
                'id': order_item.id,
                'image': article_image,
                'title': article.title,
                'price': article.price,
                'quantity': order_item.quantity,
                'stock': article.stock,
                'total': article.price * order_item.quantity,
                'slug': article.slug,
                'is_last_order_item': len(order_items) == i
            }
            print(data['is_last_order_item'])
            order_total += data['price'] * data['quantity']
            context['order_items'].append(data)
            i += i
            # print(data)
        context['empty'] = context['order_items'] == []
        context['order_total'] = order_total
        return context


class IncreaseQuantityOrderItemView(View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['id'])
        article = Article.objects.get(id=order_item.article_id)
        if verify_stock(article.stock, order_item.quantity):
            order_item.quantity += 1
            order_item.save()
        else:
            messages.warning(self.request, 'There is not enough stock')

        return redirect('cart:summary')


class DecreaseQuantityOrderItemView(View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['id'])
        if order_item.quantity == 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect('cart:summary')


class RemoveOrderItemView(View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['id'])
        order_item.delete()
        return redirect('cart:summary')
