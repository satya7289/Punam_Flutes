from django.db import models
from django.urls import reverse
from django.forms import Textarea
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Order,
    Payment,
)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'OrderNumber', 'Total', 'status', 'PaymentMethod', 'Invoice', 'created_at', 'update_at')
    list_filter = ('status', 'payment__method',)
    search_fields = ('id', 'total',)
    readonly_fields = (
        'Payment', 'Invoice',
        'Total',
        # 'country', 'currency', 'currency_code',
        'created_at', 'update_at'
    )
    fieldsets = (
        (None, {
            'fields': (
                'cart', 'billing_address', 'shipping_address', 'user', 'status',
                'Total', 'Payment', 'Invoice',
                'customization_request', 'courier_tracker',
            )
        }),
        ('Advanced Detail', {
            'classes': ('collapse',),
            'fields': (
                'coupon',
                'country', 'currency', 'currency_code',
            ),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 100})},
    }

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        for order_rel in ["cart", "billing_address", "shipping_address", "user", "coupon"]:
            field = form.base_fields[order_rel]
            field.widget.can_add_related = False
            field.widget.can_change_related = True
            field.widget.can_delete_related = False
        return form

    def Total(self, obj):
        total = obj.total if obj.total else '-'
        currency = obj.currency if (obj.total and obj.currency) else ''
        return format_html('{}{}', currency, total)

    def Payment(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.payment._meta.app_label, obj.payment._meta.model_name), args=[obj.payment.id])
        return format_html('<a href="{}">Payment Detail</a>', url, obj.payment.id)

    def PaymentMethod(self, obj):
        return obj.payment.method

    def OrderNumber(self, obj):
        return obj.id

    def Invoice(self, obj):
        if obj.status != "Pending":
            return format_html('<a href="{}">Invoice</a>', reverse('order_invoice') + '?order_id=' + str(obj.id))
        else:
            return format_html('<a href="">-</a>')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'Order', 'method', 'status', 'razorpay', 'created_at')
    list_filter = ('status', 'method')

    def Order(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.order._meta.app_label, obj.order._meta.model_name), args=[obj.order.id])
        return format_html('<a href="{}">{} Order</a>', url, obj.order.id)


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
