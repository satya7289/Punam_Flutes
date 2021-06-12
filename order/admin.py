from django import forms
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.forms import Textarea
from django.http import HttpResponse
from django.utils.html import format_html

import pandas as pd
from io import BytesIO

from .models import (
    Order,
    Payment,
    CourrierOrder,
    paymentMethod,
)


def download_sheet(data, filename):
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(xlwriter)
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)

    # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def export_as_down_to_stock(modeladmin, request, queryset):
    order_no_list = []
    payment_mode_list = []
    payment_status_list = []
    customer_name_list = []
    contact_no_list = []
    sku_list = []
    product_quantity_list = []
    filename = 'order_down_to_stock.xlsx'
    for order in queryset:
        if order.cart:
            for i, productQ in enumerate(order.cart.product_detail.all()):
                if i == 0:
                    shipping_address = order.shipping_address
                    order_no = order.id
                    customer_name = shipping_address.full_name if shipping_address else ''
                    contact_no = shipping_address.mobile_number if shipping_address else ''
                else:
                    order_no = ''
                    customer_name = ''
                    contact_no = ''
                try:
                    payment_mode = order.payment.method
                except:
                    payment_mode = ''
                try:
                    payment_status = order.payment.method
                except:
                    payment_status = ''
                sku = productQ.product.sku if productQ.product.sku else productQ.product.title
                order_no_list.append(order_no)
                payment_mode_list.append(payment_mode)
                payment_status_list.append(payment_status)
                customer_name_list.append(customer_name)
                contact_no_list.append(contact_no)
                sku_list.append(sku)
                product_quantity_list.append(productQ.quantity)
    data = {
        "Order No": order_no_list,
        "Payment Mode": payment_mode_list,
        "Payment Status" : payment_status_list,
        "Customer Name": customer_name_list,
        "Contact No": contact_no_list,
        "SKU": sku_list,
        "Product Qty": product_quantity_list,
    }

    return download_sheet(data, filename)


def export_as_ecom_soft_data(modeladmin, request, queryset):
    order_no_list = []
    product_method_list = []
    consignee_list = []
    consignee_add_list = []
    destination_city_list = []
    pincode_list = []
    state_list = []
    mobile_list = []
    item_descriptions_list = []
    pieces_list = []
    cod_amount_list = []
    declared_val_list = []
    filename = 'order_ecom_soft_data.xlsx'
    for order in queryset:
        if order.cart:
            product_desc = ''
            try:
                payment_mode = 'COD' if(order.payment.method == 'COD' and not order.payment.status) else 'Prepaid'
            except:
                payment_mode = ''
            payment_mode = 'PPD' if payment_mode == 'Prepaid' else payment_mode
            shipping_address = order.shipping_address
            if shipping_address:
                consignee_list.append(shipping_address.full_name)
                consignee_add_list.append(shipping_address.street_address)
                destination_city_list.append(shipping_address.city)
                pincode_list.append(shipping_address.postal_code)
                state_list.append(shipping_address.state)
                mobile_list.append(shipping_address.mobile_number)
            else:
                consignee_list.append('')
                consignee_add_list.append('')
                destination_city_list.append('')
                pincode_list.append('')
                state_list.append('')
                mobile_list.append('')

            cod_amount = order.total if payment_mode == 'COD' else 0
            for i, productQ in enumerate(order.cart.product_detail.all()):
                product_desc += str(productQ.quantity) + ' ' + productQ.product.title + ', '

            order_no_list.append(order.id)
            product_method_list.append(payment_mode)
            item_descriptions_list.append(product_desc)
            pieces_list.append(1)
            cod_amount_list.append(cod_amount)
            declared_val_list.append(order.total)

    data = {
        'AWB_NUMBER': '',
        'ORDER_NUMBER': order_no_list,
        'PRODUCT': product_method_list,
        'CONSIGNEE': consignee_list,
        'CONSIGNEE_ADDRESS1': consignee_add_list,
        'CONSIGNEE_ADDRESS2': '',
        'CONSIGNEE_ADDRESS3': '',
        'DESTINATION_CITY': destination_city_list,
        'PINCODE': pincode_list,
        'STATE': state_list,
        'MOBILE': mobile_list,
        'TELEPHONE': '',
        'ITEM_DESCRIPTION': item_descriptions_list,
        'PIECES': pieces_list,
        'COLLECTABLE_VALUE': cod_amount_list,
        'DECLARED_VALUE': declared_val_list,
        'ACTUAL_WEIGHT': '',
        'VOLUMETRIC_WEIGHT': '',
        'LENGTH': '',
        'BREADTH': '',
        'HEIGHT': '',
        "PICKUP_NAME": "PUNAM FLUTES",
        "PICKUP_ADDRESS_LINE1": "A 58, Jawahar Park, Deoli road, Khanpur New Delhi 110062 Phone :8505922922",
        "PICKUP_ADDRESS_LINE2": "",
        "PICKUP_PINCODE": "110062",
        "PICKUP_PHONE": "991118668",
        "PICKUP_MOBILE": "8505922922",
        "RETURN_NAME": "PUNAM FLUTES",
        "RETURN_ADDRESS_LINE1": "A 58, Jawahar Park, Deoli road, Khanpur New Delhi 110062 Phone :8505922922",
        "RETURN_ADDRESS_LINE2": "",
        "RETURN_PINCODE": "110062",
        "RETURN_PHONE": "991118668",
        "RETURN_MOBILE": "8505922922",
        'DG_SHIPMENT': '',
        'SELLER_TIN': '',
        'INVOICE_NUMBER': '',
        'INVOICE_DATE': '',
        'ESUGAM_NUMBER': '',
        "ITEM_CATEGORY": "Musical Instrument or Case",
        "PACKING_TYPE": "WH",
        "PICKUP_TYPE": "WH",
        "RETURN_TYPE": "WH",
        "CONSIGNEE_ADDRESS_TYPE": "WH",
        "PICKUP_LOCATION_CODE": "",
        "SELLER_GSTIN": "07ANLPP2290D1ZY",
        'GST_HSN': '',
        'GST_ERN': '',
        'GST_TAX_NAME': '',
        'GST_TAX_BASE': '',
        'DISCOUNT': '',
        "GST_TAX_RATE_CGSTN": "0.0",
        "GST_TAX_RATE_SGSTN": "0.0",
        "GST_TAX_RATE_IGSTN": "0.0",
        "GST_TAX_TOTAL": "0.0",
        "GST_TAX_CGSTN": "0.0",
        "GST_TAX_SGSTN": "0.0",
        "GST_TAX_IGSTN": "0.0"
    }
    return download_sheet(data, filename)


def export_as_delivery_soft_data(modeladmin, request, queryset):
    order_no_list = []
    consignee_list = []
    city_list = []
    state_list = []
    country_list = []
    consignee_add_list = []
    pincode_list = []
    mobile_list = []
    product_method_list = []
    declared_val_list = []
    cod_amount_list = []
    item_descriptions_list = []
    filename = 'order_delivery_soft_data.xlsx'
    for order in queryset:
        if order.cart:
            product_desc = ''
            try:
                payment_mode = 'COD' if(order.payment.method == 'COD' and not order.payment.status) else 'Prepaid'
            except:
                payment_mode = ''
            shipping_address = order.shipping_address
            if shipping_address:
                consignee_list.append(shipping_address.full_name)
                consignee_add_list.append(shipping_address.street_address)
                pincode_list.append(shipping_address.postal_code)
                city_list.append(shipping_address.city)
                state_list.append(shipping_address.state)
                country_list.append(shipping_address.country)
                mobile_list.append(shipping_address.mobile_number)
            else:
                consignee_list.append('')
                consignee_add_list.append('')
                pincode_list.append('')
                state_list.append('')
                mobile_list.append('')

            cod_amount = order.total if payment_mode == 'COD' else 0
            for i, productQ in enumerate(order.cart.product_detail.all()):
                product_desc += str(productQ.quantity) + ' ' + productQ.product.title + ', '

            order_no_list.append(order.id)
            product_method_list.append(payment_mode)
            item_descriptions_list.append(product_desc)
            cod_amount_list.append(cod_amount)
            declared_val_list.append(order.total)
    data = {
        'Waybill': '',
        'Reference No': order_no_list,
        'Consignee Name': consignee_list,
        'City': city_list,
        'State': state_list,
        'Country': country_list,
        'Address': consignee_add_list,
        'Pincode': pincode_list,
        'Phone': '',
        'Mobile': mobile_list,
        'Weight': '',
        'Payment Mode': product_method_list,
        'Package Amount': declared_val_list,
        'Cod Amount': cod_amount_list,
        'Product to be Shipped': item_descriptions_list,
        'Return Address': 'PUNAMEXPRESS, A 58, Jawahar Park, Deoli Road, Khanpur, New Delhi, 110062',
        'Return Pin': '110062',
        'fragile_shipment': 'true',
        'Seller Name': 'PUNAMEXPRESS ',
        'Seller Address': 'A 58 First floor Jawahar Park Deoli road Khanpur New Delhi 110062',
        'Seller CST No': '',
        'Seller TIN': '',
        'Invoice No': '',
        'Invoice Date': '',
        'Quantity': '',
        'Commodity Value': '',
        'Tax Value': '',
        'Category of Goods': 'Indigenious Handmade Musical Instruments',
        'Seller_GST_TIN': '07ANLPP2290D1ZY',
        'HSN_Code': '',
        'Return Reason': '',
        'Vendor Pickup Location': 'PUNAM EXPRESS',
        'EWBN': ''
    }
    return download_sheet(data, filename)


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
    actions = [export_as_down_to_stock, export_as_ecom_soft_data, export_as_delivery_soft_data]

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
