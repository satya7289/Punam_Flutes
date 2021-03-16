from django.db import models
from customer.models import User, Profile
from product.models import Product
from address.models import Address
from paypal.standard.ipn.models import PayPalIPN
from commons.models import TimeStampedModel
from commons.country_currency import country

paymentMethod = [['razorpay', 'razorpay'], ['paypal', 'paypal'], ['COD', 'COD']]

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
        return self.user.username + " cart" 

class Order(TimeStampedModel):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.FloatField(blank=True, null=True)
    delivered = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.profile.first_name +' '+ self.profile.last_name + ' order'
    
    class Meta:
        ordering = ("delivered",)

class Payment(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=paymentMethod, null=True, blank=True)
    paypal = models.OneToOneField(PayPalIPN, on_delete=models.CASCADE, null=True, blank=True)
    razorpay = models.CharField(max_length=25, null=True, blank=True)
    cod = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.method + ' ' + self.order.profile.first_name
    
    class Meta:
        ordering = ("status","method")

class CountryPayment(TimeStampedModel):
    country = models.CharField(max_length=100, blank=True, choices=country, null=True, default='')
    method = models.CharField(max_length=20, choices=paymentMethod, null=True, blank=True,verbose_name='Payment Method')

    def __str__(self):
        return self.country + ' ' + self.method

