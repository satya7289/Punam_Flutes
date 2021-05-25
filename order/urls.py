from django.urls import path
from django.contrib.auth.decorators import login_required

from .views.payment import (
    payment_done,
    payment_canceled,
    process_payment,
    razorpay_done,
    razorpay_cancel,
)

from .views.order import (
    OrderList,
    OrderDetail,
    CancelOrder,
)

from .views.invoice import (
    OrderInvoice,
)

from .views.courrier import (
    CheckForCourrier,
    CreateOrderForCourrier,
    TrackCourrierOrder
)

urlpatterns = [
    path('', login_required(OrderList.as_view()), name='orders'),
    path('order-detail-<int:order_id>', login_required(OrderDetail.as_view()), name='order_detail'),
    path('order-cencel', login_required(CancelOrder.as_view()), name='order_cancel'),

    # Invoice Related
    path('order-invoice', login_required(OrderInvoice.as_view()), name='order_invoice'),

    # Courrier Related
    path('check-for-courrier', CheckForCourrier.as_view(), name='check_for_courrier'),
    path('create-order-for-courrier', CreateOrderForCourrier.as_view(), name='create_order_for_courrier'),
    path('track-courrier-order', TrackCourrierOrder.as_view(), name='track_courrier_order'),

    # Payment Related
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('razorpay-done/', razorpay_done, name='razorpay_done'),
    path('razorpay-cancel', razorpay_cancel, name='razorpay_cancel'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]
