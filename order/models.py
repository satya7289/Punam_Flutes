from django.db import models

from customer.models import User
from cart.models import Cart
from address.models import Address
from coupon.models import Coupon
from paypal.standard.ipn.models import PayPalIPN
from commons.models import TimeStampedModel


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


class Order(TimeStampedModel):
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="billing_address", blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="shipping_address", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    customization_request = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=OrderStatus, blank=True, null=True)
    courier_tracker = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'order#' + str(self.id)

    class Meta:
        ordering = ("created_at",)


class Payment(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, blank=True, null=True)
    method = models.CharField(max_length=20, choices=paymentMethod, null=True, blank=True)
    paypal = models.OneToOneField(PayPalIPN, on_delete=models.SET_NULL, null=True, blank=True)
    razorpay = models.CharField(max_length=25, null=True, blank=True)
    cod = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.method + ' '

    class Meta:
        ordering = ("status", "method")
