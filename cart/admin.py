
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Cart, 
    ProductQuantity
)


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


admin.site.register(Cart, CartAdmin)
admin.site.register(ProductQuantity)
