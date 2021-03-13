from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .views import AddToCart
from .views import RemoveFromCart
from .views import CartView
from .views import Checkout
from .views import OrderList
from .views import payment_done, payment_canceled, process_payment, razorpay_done, razorpay_cancel

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_to_cart/', login_required(AddToCart.as_view()), name='add_to_cart'),
    path('remove_from_cart/', login_required(RemoveFromCart.as_view()), name='remove_from_cart'),
    path('checkout/', login_required(Checkout.as_view()), name='checkout'),
    path('order/', login_required(OrderList.as_view()), name='orders'),
    
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('razorpay-done/', razorpay_done, name='razorpay_done'),
    path('razorpay-cancel', razorpay_cancel, name='razorpay_cancel'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]
