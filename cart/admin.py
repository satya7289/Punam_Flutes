from django.contrib import admin
from .models import Cart, ProductQuantity, Checkout

admin.site.register(Cart)
admin.site.register(ProductQuantity)
admin.site.register(Checkout)
