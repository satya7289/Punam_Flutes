from django.db import models
from customer.models import User
from product.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    is_checkout = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " " + str(self.is_checkout)
