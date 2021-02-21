from django.db import models
from customer.models import User, Profile
from product.models import Product
from address.models import Address
from paypal.standard.ipn.models import PayPalIPN
from commons.models import TimeStampedModel

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
        return self.user.email + " " + str(self.is_checkout)

class Order(TimeStampedModel):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    total = models.FloatField(blank=True, null=True)
    delivered = models.BooleanField(default=False, null=True)
    payment = models.OneToOneField(PayPalIPN, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.profile.first_name +' '+ self.profile.last_name

