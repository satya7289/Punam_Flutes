import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from cart.models import Cart
from order.models import Order
from commons.mail import SendEmail
from tax_rules.views import CalculateTaxForCart
from commons.product_price import get_price_of_product


def is_cart_availabe(user):
    cart = Cart.objects.filter(user=user, is_checkout=False).first()

    # If cart exits
    if cart:
        return True
    return False


def get_cart(user):
    return Cart.objects.filter(user=user, is_checkout=False).first()


def update_order_for_additional_data(order):
    order.country = settings.COUNTRY
    order.currency = settings.CURRENCY_SYMBOL
    order.currency_code = settings.CURRENCY_CODE
    order.save()
    return order


def get_order(user):
    cart = Cart.objects.filter(user=user, is_checkout=False).first()

    # If cart exits
    if cart:
        order = Order.objects.filter(cart=cart).first()
        # If order exits
        if order:
            return order
    return None


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
        try:
            if product.inventory:
                product.inventory.sold = product.inventory.sold + productQ.quantity
                if product.inventory.type == "limited":
                    product.inventory.available = product.inventory.available - productQ.quantity
                product.inventory.save()
        except ObjectDoesNotExist:
            pass

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
        user = order.user

        product_details = order.cart.product_detail.all()
        currency = settings.CURRENCY_SYMBOL

        # Add the price and currency according to the user's location to the product
        for product in product_details:
            price_list = get_price_of_product(request, product.product)
            product.price = price_list['price']

        data = {
            'products': product_details,
            'total': order.total,
            'shipping_address': order.shipping_address,
            'currency': currency,
            'totalTax': json.loads(CalculateTaxForCart(request, order.cart.id, order.shipping_address.id).content)['totalTax'],
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
