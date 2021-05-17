
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Cart,
    ProductQuantity
)


class ProductQuantityInLine(admin.TabularInline):
    model = Cart.product_detail.through
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'User', 'is_checkout', 'created_at')
    list_filter = ('is_checkout', )
    exclude = ('product_detail', )
    inlines = [
        ProductQuantityInLine,
    ]
    readonly_fields = ('R_user', 'created_at', 'update_at')
    fieldsets = (
        (None, {
            'fields': (
                'R_user',
                'is_checkout',
            )
        }),
        ('Advanced Detail', {
            'classes': ('collapse',),
            'fields': (
                'created_at', 'update_at',
            ),
        }),
    )

    def User(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name), args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user)

    def R_user(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name), args=[obj.user.id])
        return format_html('{}<a style="padding:5px" href="{}"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>', obj.user, url)

    R_user.short_description = 'User'


class ProductQuantityAdmin(admin.ModelAdmin):
    autocomplete_fields = ('product',)


admin.site.register(Cart, CartAdmin)
admin.site.register(ProductQuantity, ProductQuantityAdmin)
