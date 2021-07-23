from django.urls import path
from core.cart.views import CartView, DecreaseQuantityOrderItemView, IncreaseQuantityOrderItemView, RemoveOrderItemView

app_name = 'cart'
urlpatterns = [
    path('', CartView.as_view(), name='summary'),
    path('item/increase/<uuid:id>',
         IncreaseQuantityOrderItemView.as_view(),
         name='item-increase'),
    path('item/decrease/<uuid:id>',
         DecreaseQuantityOrderItemView.as_view(),
         name='item-decrease'),
    path('item/remove/<uuid:id>',
         RemoveOrderItemView.as_view(),
         name='item-remove')
]
