from django.db import models

from customer.models import User
from cart.models import Cart
from address.models import Address
from coupon.models import Coupon
from paypal.standard.ipn.models import PayPalIPN
from commons.models import TimeStampedModel

from .utils import orderStatusChangeNotification

paymentMethod = [['razorpay', 'razorpay'], ['paypal', 'paypal'], ['COD', 'COD']]
OrderStatus = [
    ['Pending', 'Pending'],
    ['Confirmed', 'Confirmed'],
    ['Paid', 'Paid'],
    ['Dispatch', 'Dispatch'],
    ['Shipped', 'Shipped'],
    ['Delivered', 'Delivered'],
    ['Canceled', 'Canceled'],
    ['Refunded', 'Refunded']
]
CourrierOption = [
    ['Delhivery', 'Delhivery']
]


class Order(TimeStampedModel):
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="billing_address", blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="shipping_address", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=50, choices=OrderStatus, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    customization_request = models.TextField(blank=True, null=True)
    courier_tracker = models.TextField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=512, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    order_placed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'order#' + str(self.id)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        orderStatusChangeNotification(self)
        return super().save()


class Payment(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, blank=True, null=True)
    method = models.CharField(max_length=20, choices=paymentMethod, null=True, blank=True)
    paypal = models.OneToOneField(PayPalIPN, on_delete=models.SET_NULL, null=True, blank=True)
    razorpay = models.CharField(max_length=25, null=True, blank=True)
    cod = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'payment#{self.id}'

    class Meta:
        ordering = ("status", "method")


class CourrierOrder(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, blank=True, null=True)
    courrier = models.CharField(max_length=255, blank=True, null=True)
    tracking_number = models.CharField(max_length=1024, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'courrier#{self.id}'
