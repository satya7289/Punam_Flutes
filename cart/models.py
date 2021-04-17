from django.db import models
from customer.models import User, Profile
from product.models import Product
from address.models import Address
from paypal.standard.ipn.models import PayPalIPN
from commons.models import TimeStampedModel
from commons.country_currency import country
from coupon.models import Coupon

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

    def __str__(self):
        return str(self.quantity) + ' ' + str(self.product.title)
    

class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_detail = models.ManyToManyField(ProductQuantity)
    is_checkout = models.BooleanField(default=False)

    def __str__(self):
        return "cart#" + str(self.id) 

class Order(TimeStampedModel):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="billing_address", blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="shipping_address", blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.FloatField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=OrderStatus ,blank=True, null=True)

    def __str__(self):
        return 'order#'+ str(self.id)
    
    class Meta:
        ordering = ("created_at",)

class Payment(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=paymentMethod, null=True, blank=True)
    paypal = models.OneToOneField(PayPalIPN, on_delete=models.CASCADE, null=True, blank=True)
    razorpay = models.CharField(max_length=25, null=True, blank=True)
    cod = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.method + ' ' + self.order.profile.user.username
    
    class Meta:
        ordering = ("status","method")

class CountryPayment(TimeStampedModel):
    country = models.CharField(max_length=100, blank=True, choices=country, null=True, default='')
    razorpay = models.BooleanField(default=True, blank=True, null=True)
    paypal = models.BooleanField(default=True, blank=True, null=True)
    cod = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.country

