from django.contrib import admin
from .models import Cart, ProductQuantity, Order

admin.site.register(Cart)
admin.site.register(ProductQuantity)
admin.site.register(Order)
