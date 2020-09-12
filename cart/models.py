from django.db import models
from customer.models import User, Profile
from product.models import Product
from address.models import Address

class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.quantity) + ' ' + str(self.product.title)
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_detail = models.ManyToManyField(ProductQuantity)
    is_checkout = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    update_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.user.email + " " + str(self.is_checkout)

class Checkout(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    update_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.profile
