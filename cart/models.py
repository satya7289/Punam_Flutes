from django.db import models

from customer.models import User
from product.models import Product
from commons.models import TimeStampedModel
from commons.product_price import get_price_of_product

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
    country = models.CharField(max_length=512, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.quantity) + ' ' + str(self.product.title)

    def save(self, *args, **kwargs):
        product_price = get_price_of_product(self.product)
        amount = float(product_price['price']) * int(self.quantity)
        if amount != 0:
            self.amount = amount
        return super().save()


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_detail = models.ManyToManyField(ProductQuantity)
    is_checkout = models.BooleanField(default=False)

    def __str__(self):
        return "cart#" + str(self.id)
