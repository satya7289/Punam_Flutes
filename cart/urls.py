from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from .views import (
    AddToCart,
    RemoveFromCart,
    CartView,
    Checkout,
    ChooseShippingAddress,
    ChooseBillingAddress,
    ProcessToCheckout,
)

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_to_cart/', login_required(AddToCart.as_view()), name='add_to_cart'),
    path('remove_from_cart/', login_required(RemoveFromCart.as_view()), name='remove_from_cart'),
    path('process-to-checkout', login_required(ProcessToCheckout.as_view()), name='process_to_checkout'),
    path('choose-shipping-address',login_required(ChooseShippingAddress.as_view()), name='choose_shipping_address'),
    path('choose-billing-address',login_required(ChooseBillingAddress.as_view()), name='choose_billing_address'),
    path('checkout/', login_required(Checkout.as_view()), name='checkout'),
]
