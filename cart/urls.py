from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from .views import (
    AddToCart,
    RemoveFromCart,
    CartView,
    Checkout,
    OrderList,
    sendInvoice,
    CancelOrder,
    OrderInvoice,
    ChooseShippingAddress,
    ChooseBillingAddress,
    ProcessToCheckout,
)

from .views import (
    payment_done, 
    payment_canceled, 
    process_payment, 
    razorpay_done, 
    razorpay_cancel,
)

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_to_cart/', login_required(AddToCart.as_view()), name='add_to_cart'),
    path('remove_from_cart/', login_required(RemoveFromCart.as_view()), name='remove_from_cart'),
    path('process-to-checkout', login_required(ProcessToCheckout.as_view()), name='process_to_checkout'),
    path('choose-shipping-address',login_required(ChooseShippingAddress.as_view()), name='choose_shipping_address'),
    path('choose-billing-address',login_required(ChooseBillingAddress.as_view()), name='choose_billing_address'),
    path('checkout/', login_required(Checkout.as_view()), name='checkout'),
    path('order/', login_required(OrderList.as_view()), name='orders'),
    path('order-cencel', login_required(CancelOrder.as_view()), name='order_cancel'),
    path('order-invoice', login_required(OrderInvoice.as_view()), name='order_invoice'),
    
    # path('sendInvoice', sendInvoice, name='send-invoice'),

    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('razorpay-done/', razorpay_done, name='razorpay_done'),
    path('razorpay-cancel', razorpay_cancel, name='razorpay_cancel'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]
