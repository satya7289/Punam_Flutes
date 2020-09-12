from django.urls import path
from django.views.generic.base import TemplateView

from .views import AddToCart
from .views import RemoveFromCart
from .views import CartView
from .views import Checkout
from .views import payment_done, payment_canceled, process_payment

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_to_cart/', AddToCart.as_view(), name='add_to_cart'),
    path('remove_from_cart/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]
