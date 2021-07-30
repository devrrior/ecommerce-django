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

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = 'cart/success.html'

class CancelView(TemplateView):
    template_name = 'cart/cancel.html'



class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(customer_id=self.request.user.id, ordered=False)  # type: ignore
        # order_items = order.orderitem_set.all().order_by('-id')
        order_item = order.orderitem_set.first()
        # articles = Article.objects.all()
        article = Article.objects.get(id=order_item.article_id)
        # order_item = OrderItem.objects.first()  # type:ignore
        YOUR_DOMAIN = 'http://127.0.0.1:8000'
        
#         for order_item in order_items:
#             article = articles.filter(id=order_item.article_id).first()
# 
#             line_item = {
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': article.price,
#                         'product_data': {
#                             'name': article.title,
#                             # 'images': ''
#                         },
#                     },
#                     'quantity': order_item.quantity,
#                 },
#             }
# 
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=[
                    'card',
                ],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': article.price,
                            'product_data': {
                                'name': article.title,
                                'images': ['https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.mediaexpert.pl%2Fmedia%2Fcache%2Fresolve%2Ffilemanager_original%2Fimages%2Fdescriptions%2Fimages%2F21%2F2151973%2Fstorage_app_opisy2_huawei_562389%2Fhuawei_matebook_d14_8_pami____.jpg&f=1&nofb=1',]
                            },
                        },
                        'quantity': order_item.quantity,
                    },
                ],
                mode='payment',
                success_url = YOUR_DOMAIN + '/success',
                cancel_url = YOUR_DOMAIN + '/cancel',
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
            }
            order_total += data['price'] * data['quantity']
            context['order_items'].append(data)
            i += i
        context['empty'] = context['order_items'] == []
        context['order_total_without_iva'] = order_total
        context['order_total_with_iva'] = round((order_total * 0.16) + order_total, 2)
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
