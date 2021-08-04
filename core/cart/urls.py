from django.urls import path
from core.cart.views import (
    CancelView,
    CartView,
    DecreaseQuantityOrderItemView,
    IncreaseQuantityOrderItemView,
    RemoveOrderItemView,
    Checkout,
    CreateCheckoutSessionView,
    SuccessView,
)

app_name = 'cart'
urlpatterns = [
    path('cart/', CartView.as_view(), name='summary'),
    path(
        'cart/item/increase/<uuid:id>',
        IncreaseQuantityOrderItemView.as_view(),
        name='item-increase',
    ),
    path(
        'cart/item/decrease/<uuid:id>',
        DecreaseQuantityOrderItemView.as_view(),
        name='item-decrease',
    ),
    path(
        'cart/item/remove/<uuid:id>', RemoveOrderItemView.as_view(), name='item-remove'
    ),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('order/success/', SuccessView.as_view(), name='process-succeed'),
    path('order/cancel/', CancelView.as_view(), name='process-canceled'),
    path(
        'create-checkout-session/',
        CreateCheckoutSessionView.as_view(),
        name='create-checkout-session',
    ),
]
