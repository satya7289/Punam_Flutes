
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, ProductQuantity, Order, Payment, CountryPayment


class ProductQuantityInLine(admin.TabularInline):
    model = Cart.product_detail.through
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'User', 'is_checkout', 'created_at')
    list_filter = ('is_checkout', )
    exclude = ('product_detail', )
    inlines = [
        ProductQuantityInLine,
    ]

    def User(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label,  obj.user._meta.model_name),  args=[obj.user.id] )
        return format_html('<a href="{}">{}</a>', url, obj.user)
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'total', 'status', 'Payment', 'PaymentMethod', 'notes', 'coupon', 'shipping_address', 'billing_address', 'created_at', 'Invoice')
    list_filter = ('status', )
    search_fields = ('notes', 'total',)

    def Payment(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.payment._meta.app_label,  obj.payment._meta.model_name),  args=[obj.payment.id] )
        return format_html('<a href="{}">Payment</a>', url, obj.payment.id)
    
    def PaymentMethod(self, obj):
        return obj.payment.method

    def Invoice(self, obj):
        return format_html('<a href="{}">Invoice</a>', reverse('order_invoice') + '?order_id=' + str(obj.id))


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'Order', 'method', 'status', 'razorpay', 'created_at')
    list_filter = ('status', 'method')

    def Order(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.order._meta.app_label,  obj.order._meta.model_name),  args=[obj.order.id] )
        return format_html('<a href="{}">{} Order</a>', url, obj.order.id)

class CountryPaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'country', 'razorpay', 'paypal', 'cod')
    list_filter = ( 'razorpay', 'paypal', 'cod', 'country')

admin.site.register(Cart, CartAdmin)
admin.site.register(ProductQuantity)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CountryPayment, CountryPaymentAdmin)
