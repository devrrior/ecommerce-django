import stripe
from core.articles.models import Article
from core.cart.models import Order, OrderItem
from core.cart.utils import verify_stock
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = 'cart/success.html'

class CancelView(TemplateView):
    template_name = 'cart/cancel.html'



class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(customer_id=self.request.user.id, ordered=False)  # type: ignore
        order_items = order.orderitem_set.all().order_by('-id')
        articles = Article.objects.all()
        line_items = []

        for item in order_items:
            article = articles.filter(id=item.article_id).first()
            price_object = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': article.price,
                    'product_data': {
                        'name': article.title[:60]
                    }
                },
                'quantity': item.quantity
            }
            line_items.append(price_object)


        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email = self.request.user.email,
                billing_address_collection='auto',
                shipping_rates = ['shr_1JJ21wH70q2DLVwFniELrAcf'],
                shipping_address_collection={

                  'allowed_countries': ['US', 'CA', 'MX'],

                },
                payment_method_types=['card',],
                line_items = line_items,
                mode='payment',
                success_url = self.request.build_absolute_uri(reverse('cart:process-succeed')),
                cancel_url = self.request.build_absolute_uri(reverse('cart:process-canceled')),
            )

        except Exception as e:
            print(e)
            return str(e)

        return redirect(checkout_session.url)


class Checkout(TemplateView):
    template_name = 'cart/checkout.html'

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        return context


class CartView(TemplateView):
    template_name = 'cart/summary.html'

    # TODO conseguir solo los datos que quiere
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['order_items'] = []
        articles = Article.objects.all().only()

        try:
            order = Order.objects.get(customer_id=self.request.user.id, ordered=False) # type: ignore
        except ObjectDoesNotExist:
            context['empty'] = True
            return context

        order_items = order.orderitem_set.all().order_by('-id')
        order_total = 0

        index_last_item = len(order_items)
        i = 0
        for order_item in order_items:

            i += 1

            article = articles.filter(id=order_item.article_id).first()
            article_image = article.imagearticle_set.get(order=1).image
            data = {
                'id': order_item.id,
                'image': article_image,
                'title': article.title,
                'price': article.get_display_price,
                'quantity': order_item.quantity,
                'stock': article.stock,
                'total': article.price * order_item.quantity,
                'slug': article.slug,
            }
            if i == index_last_item:
                data['last_item'] = True
            else:
                data['last_item'] = False

            order_total += data['price'] * data['quantity']
            context['order_items'].append(data)

        context['empty'] = context['order_items'] == []
        context['order_total'] = order_total
        context['length_order_items'] = len(order_items)
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
