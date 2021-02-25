from django.db import models
from customer.models import User, Profile
from product.models import Product
from address.models import Address
from paypal.standard.ipn.models import PayPalIPN
from commons.models import TimeStampedModel

paymentMethod = [['razorpay', 'razorpay'], ['paypal', 'paypal']]

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
        return self.user.email + " cart" 

class Order(TimeStampedModel):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.FloatField(blank=True, null=True)
    delivered = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.profile.first_name +' '+ self.profile.last_name

class Payment(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=paymentMethod, null=True, blank=True)
    paypal = models.OneToOneField(PayPalIPN, on_delete=models.CASCADE, null=True, blank=True)
    razorpay = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.method + ' ' + self.order.profile.first_name 
    