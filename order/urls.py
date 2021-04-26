from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .views import (
    payment_done, 
    payment_canceled, 
    process_payment, 
    razorpay_done, 
    razorpay_cancel,
)

from .views import (
    OrderList,
    sendInvoice,
    CancelOrder,
    OrderInvoice,
)

urlpatterns = [
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
