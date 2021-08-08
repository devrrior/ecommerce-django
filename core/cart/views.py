import stripe
from logger_case import logger
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
    template_name = "cart/success.html"


class CancelView(TemplateView):
    template_name = "cart/cancel.html"


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(customer_id=self.request.user.id, ordered=False)  # type: ignore
        order_items = order.orderitem_set.all().order_by("-id")
        articles = Article.objects.all()
        line_items = []

        for item in order_items:
            article = articles.filter(id=item.article_id).first()
            price_object = {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": article.price,
                    "product_data": {"name": article.title[:60]},
                },
                "quantity": item.quantity,
            }
            line_items.append(price_object)

        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=self.request.user.email,
                billing_address_collection="auto",
                shipping_rates=["shr_1JJ21wH70q2DLVwFniELrAcf"],
                shipping_address_collection={
                    "allowed_countries": ["US", "CA", "MX"],
                },
                payment_method_types=[
                    "card",
                ],
                line_items=line_items,
                mode="payment",
                success_url=self.request.build_absolute_uri(
                    reverse("cart:process-succeed")
                ),
                cancel_url=self.request.build_absolute_uri(
                    reverse("cart:process-canceled")
                ),
            )

        except Exception as e:
            print(e)
            return str(e)

        return redirect(checkout_session.url)


class Checkout(TemplateView):
    template_name = "cart/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        return context


class CartView(TemplateView):
    template_name = "cart/summary.html"

    # TODO conseguir solo los datos que quiere
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        order_items = OrderItem.objects.filter(
            order__customer=self.request.user, order__ordered=False
        ).select_related("article")
        length_order_items = len(order_items)
        context["length_order_items"] = length_order_items
        context["order_items"] = []

        if length_order_items == 0:
            context["empty"] = True
            return context

        i = 0
        for order_item in order_items:

            i += 1

            article_image = order_item.article.imagearticle_set.get(order=1).image
            data = {
                "id": order_item.id,
                "image": article_image,
                "title": order_item.article.title,
                "price": order_item.article.get_display_price,
                "quantity": order_item.quantity,
                "stock": order_item.article.stock,
                "total": order_item.article.price * order_item.quantity,
                "slug": order_item.article.slug,
            }
            if i == length_order_items:
                data["last_item"] = True

            context["order_total"] = data["price"] * data["quantity"]
            context["order_items"].append(data)

        return context


class IncreaseQuantityOrderItemView(View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs["id"])
        article = Article.objects.get(id=order_item.article_id)
        if verify_stock(article.stock, order_item.quantity):
            order_item.quantity += 1
            order_item.save()
        else:
            messages.warning(self.request, "There is not enough stock")

        return redirect("cart:summary")


class DecreaseQuantityOrderItemView(View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs["id"])
        if order_item.quantity == 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("cart:summary")


class RemoveOrderItemView(View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs["id"])
        order_item.delete()
        return redirect("cart:summary")
