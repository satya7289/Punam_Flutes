from django.db import models
from customer.models import User
from product.models import Product
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


class ProductQuantity(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.FloatField(blank=True, null=True)
    tax_amount = models.FloatField(blank=True, null=True)
    coupon_amount = models.FloatField(blank=True, null=True)
    shipping_amount = models.FloatField(blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.quantity) + ' ' + str(self.product.title)


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_detail = models.ManyToManyField(ProductQuantity)
    is_checkout = models.BooleanField(default=False)

    def __str__(self):
        return "cart#" + str(self.id)
