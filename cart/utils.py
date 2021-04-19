from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.html import format_html

from cart.models import Cart, ProductQuantity, Order, Payment, CountryPayment
from customer.models import User
from customer.models import Profile
from product.models import Product
from coupon.models import Coupon
from commons.product_price import get_price_of_product, get_ip_detail
from address.models import Address
from commons.mail import SendEmail
from tax_rules.models import TaxRule, GSTState
import razorpay
from tax_rules.views import CalculateTaxForCart
import json

def after_successful_placed_order(request, payment, order_status="Confirmed"):
    '''
    @param: request
    @param: payment (model)
    @param: order_status (str)
    '''

    order = payment.order
    cart = payment.order.cart
    coupon = payment.order.coupon

    # Update the Ordered product inventory
    for productQ in cart.product_detail.all():
        product = productQ.product
        product.inventory.sold = product.inventory.sold + productQ.quantity
        product.inventory.available = product.inventory.available - productQ.quantity
        product.inventory.save()
    
    # Set Cart checkout to True.
    cart.is_checkout = True
    cart.save()

    # Update the status of the coupon if applied.
    order.status = order_status
    order.save()

    # Update the status of the order.
    if coupon:
        coupon.coupon_used = coupon.coupon_used + 1
        coupon.save()

    # Send notification for order is placed.
    notification = placed_order_notification(request, order.id)

    return notification


def placed_order_notification(request, orderId):
    order = Order.objects.filter(id=orderId).first()
    message = "order is not created"
    if order:
        user = order.profile.user

        product_details = order.cart.product_detail.all()
        currency = settings.DEFAULT_CURRENCY

        # Add the price and currency according to the user's location to the product
        for product in product_details:
            price_list = get_price_of_product(request,product.product)
            product.price = price_list['price']
            product.currency = price_list['currency']
            currency = price_list['currency']
        
        data = {
            'products': product_details,
            'total': order.total,
            'shipping_address': order.shipping_address,
            'totalTax': json.loads(CalculateTaxForCart(request, order.cart.id, order.shipping_address.id).content)['totalTax'],
            'currency': currency
        }
        # return render(request, 'invoice.html', context=data)
        if user.email and user.email_verified:
            sendEmail = SendEmail('invoice.html', data, 'Your Invoice')
            sendEmail.send((user.email,))
            message = "Invoice sent"
        else:
            message = "either email is not there or email not verified."
        
        if user.phone and user.phone_verified:
            # TODO send Mobile sms
            message = "inbox sent"
            pass
        else:
            message = "either phone is not there or phone not verified."
        return message
    return message