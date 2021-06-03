from django import forms
from django.db import models
from django.urls import reverse
from django.forms import Textarea
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Order,
    Payment,
    CourrierOrder,
    paymentMethod,
)


class OrderAdmin(admin.ModelAdmin):
    change_form_template = 'order/change_form.html'
    list_display = ('__str__', 'OrderNumber', 'Total', 'status', 'PaymentMethod', 'Invoice', 'User', 'created_at', 'update_at')
    list_filter = ('status', 'payment__method',)
    search_fields = ('id', 'total',)
    readonly_fields = (
        'R_cart', 'R_billing_address', 'R_shipping_address', 'R_user', 'currency',
        'Payment', 'Invoice', 'Courrier',
        'CourrierName', 'TrackingNumber',
        'TrackDelivery',
        'Total',
        'created_at', 'update_at',
        'order_placed',
    )
    fieldsets = (
        (None, {
            'fields': (
                'R_cart', 'R_billing_address', 'R_shipping_address', 'R_user', 'status',
                ('total', 'currency'),
                ('customization_request', 'courier_tracker'),
                'Payment', 'Invoice', 'Courrier',
                'TrackDelivery',
            )
        }),
        ('Advanced Detail', {
            'classes': ('collapse',),
            'fields': (
                'coupon',
                'country', 'currency_code',
                'CourrierName', 'TrackingNumber',
                'created_at', 'update_at', 'order_placed'
            ),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 50})},
    }

    def Total(self, obj):
        total = obj.total if obj.total else '-'
        currency = obj.currency if (obj.total and obj.currency) else ''
        return format_html('{}{}', currency, total)

    def Payment(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.payment._meta.app_label, obj.payment._meta.model_name), args=[obj.payment.id])
        return format_html('<a href="{}">Payment Detail</a>', url, obj.payment.id)

    def Courrier(self, obj):
        try:
            if obj.courrierorder:
                courrierOrder = obj.courrierorder
                if courrierOrder.tracking_number:
                    if courrierOrder.courrier.lower() == 'delhivery':
                        return 'Courrier Booked'
                    elif courrierOrder.courrier.lower() == 'ecom' and courrierOrder.courrier_booked_status:
                        return 'Courrier Booked'
        except:
            pass
        return format_html('<a id="check_courrier" data-id="{}" href="javascript:void(null)">Check Courrier Services</a>', obj.id)

    def TrackDelivery(self, obj):
        try:
            if obj.courrierorder:
                courrierOrder = obj.courrierorder
                if courrierOrder.tracking_number:
                    if courrierOrder.courrier.lower() == 'delhivery':
                        return format_html('<a id="tracking" data-order_id="{}" href="javascript:void(null)">Track Delivery</a>', obj.id)
                    elif courrierOrder.courrier.lower() == 'ecom' and courrierOrder.courrier_booked_status:
                        return format_html('<a id="tracking" data-order_id="{}" href="javascript:void(null)">Track Delivery</a>', obj.id)              
        except:
            pass
        return '-'

    def CourrierName(self, obj):
        if obj.courrierorder:
            return obj.courrierorder.courrier if obj.courrierorder.courrier else '-'

    def TrackingNumber(self, obj):
        if obj.courrierorder:
            return obj.courrierorder.tracking_number if obj.courrierorder.tracking_number else '-'

    def PaymentMethod(self, obj):
        return obj.payment.method

    def OrderNumber(self, obj):
        return obj.id

    def Invoice(self, obj):
        if obj.status != "Pending":
            return format_html('<a href="{}"  target="_blank" rel="noopener noreferrer">Invoice</a>', reverse('order_invoice') + '?order_id=' + str(obj.id))
        else:
            return format_html('<a href="">-</a>')

    def R_cart(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.cart._meta.app_label, obj.cart._meta.model_name), args=[obj.cart.id])
        return format_html('{}<a style="padding:5px" href="{}"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>', obj.cart, url)

    def R_billing_address(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.billing_address._meta.app_label, obj.billing_address._meta.model_name), args=[obj.billing_address.id])
        return format_html('{}<a style="padding:5px" href="{}"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>', obj.billing_address, url)

    def R_shipping_address(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.shipping_address._meta.app_label, obj.shipping_address._meta.model_name), args=[obj.shipping_address.id])
        return format_html('{}<a style="padding:5px" href="{}"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>', obj.shipping_address, url)

    def R_user(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name), args=[obj.user.id])
        return format_html('{}<a style="padding:5px" href="{}"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>', obj.user, url)

    def User(self, obj):
        if obj.cart:
            return obj.cart.user

    R_cart.short_description = 'Cart'
    R_billing_address.short_description = 'Billing address'
    R_shipping_address.short_description = 'Shipping address'
    R_user.short_description = 'User'
    Payment.short_description = 'Payment'
    Invoice.short_description = 'Invoice'
    Courrier.short_description = 'Courrier Services'
    CourrierName.short_description = 'Courrier Name'
    TrackingNumber.short_description = 'Tracking Number'
    TrackDelivery.short_description = 'Track Delivery Status'


class PaymentAdminForm(forms.ModelForm):
    method = forms.ChoiceField(choices=paymentMethod)
    method_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'If method is other specify method name'}), required=False)

    class Meta:
        models = Payment
        fields = '__all__'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'Order', 'method', 'status', 'razorpay', 'created_at')
    list_filter = ('status', 'method')

    form = PaymentAdminForm

    def Order(self, obj):
        if obj.order:
            url = reverse('admin:%s_%s_change' % (obj.order._meta.app_label, obj.order._meta.model_name), args=[obj.order.id])
            return format_html('<a href="{}">{} Order</a>', url, obj.order.id)


class CourrierOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'courrier', 'order', 'tracking_number')
    ordering = ('-created_at',)


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CourrierOrder, CourrierOrderAdmin)
