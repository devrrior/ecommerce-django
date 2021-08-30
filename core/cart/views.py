import stripe
from core.articles.models import Article
from core.cart.models import Order, OrderItem
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = 'cart/success.html'


class CancelView(TemplateView):
    template_name = 'cart/cancel.html'


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(
            customer_id=self.request.user.id, ordered=False)
        order_items = order.orderitems.all().order_by('-id')
        articles = Article.objects.all()
        line_items = []

        for item in order_items:
            article = articles.filter(id=item.article_id).first()
            price_object = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': article.price,
                    'product_data': {
                        'name': article.title[:60],
                    },
                },
                'quantity': item.quantity,
            }
            line_items.append(price_object)

        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=self.request.user.email,
                billing_address_collection='auto',
                shipping_rates=['shr_1JJ21wH70q2DLVwFniELrAcf'],
                shipping_address_collection={
                    'allowed_countries': ['US', 'CA', 'MX'],
                },
                payment_method_types=[
                    'card',
                ],
                line_items=line_items,
                metadata={
                    'order_id': order.id
                },
                mode='payment',
                success_url=self.request.build_absolute_uri(
                    reverse('cart:process-succeed')
                ),
                cancel_url=self.request.build_absolute_uri(
                    reverse('cart:process-canceled')
                ),
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
        order_items = (
            OrderItem.objects.select_related('article')  # type:ignore
            .prefetch_related('article__imagearticles')
            .filter(order__customer=self.request.user, order__ordered=False)
        )
        length_order_items = len(order_items)
        context['length_order_items'] = length_order_items
        context['order_items'] = []
        context['order_total'] = 0

        if length_order_items == 0:
            context['empty'] = True
            return context

        i = 0
        for order_item in order_items:

            i += 1

            article_image = order_item.article.imagearticles.get(order=1).image
            data = {
                'id': order_item.id,
                'image': article_image,
                'title': order_item.article.title,
                'price': order_item.article.get_display_price,
                'quantity': order_item.quantity,
                'stock': order_item.article.stock,
                'total': order_item.article.price * order_item.quantity,
                'slug': order_item.article.slug,
            }
            if i == length_order_items:
                data['last_item'] = True

            context['order_total'] += data['price'] * data['quantity']
            context['order_items'].append(data)

        return context


class IncreaseQuantityOrderItemView(View):
    def get(self, request, *args, **kwargs):
        order_item = OrderItem.objects.select_related('article').get(
            id=kwargs['id'])
        article = order_item.article

        if article.stock >= order_item.quantity + 1:
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


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session['customer_details']['email']

        order_id = session['metadata']['order_id']
        order = Order.objects.get(id=order_id)
        order.ordered = True
        order.save()
        order_items = order.orderitems.all()

        amount_total = session['amount_total'] / 100
        order_items_data = []

        for item in order_items:
            item.item_sold()
            order_item = {
                'title': item.article.title[:90] + '...',
                'price': item.article.price / 100,
                'quantity': item.quantity,
                'total': (item.article.price / 100) * item.quantity,
            }

            order_items_data.append(order_item)

        context = {
            'amount_total': amount_total,
            'updated_at': order.updated_at,
            'order_items': order_items_data,
            'name': order.customer.first_name,
        }

        template = get_template('cart/success_purchase.html')
        content = template.render(context)
        email = EmailMultiAlternatives(
            f'Success purchase! Your order id is {order_id}',
            'Test',
            settings.EMAIL_HOST_USER,
            [customer_email]
        )

        email.attach_alternative(content, 'text/html')
        email.send()

    # Passed signature verification
    return HttpResponse(status=200)
