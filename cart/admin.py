from django.contrib import admin
from .models import Cart, ProductQuantity, Order, Payment

class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'user', 'is_checkout', 'created_at')
    list_filter = ('is_checkout', )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'cart', 'profile', 'total', 'delivered', 'created_at')
    list_filter = ('delivered', )

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'order', 'method', 'status', 'razorpay', 'created_at')
    list_filter = ('status', 'method')

admin.site.register(Cart, CartAdmin)
admin.site.register(ProductQuantity)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
