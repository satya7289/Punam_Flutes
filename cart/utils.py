import json
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from cart.models import Cart
from order.models import Order
from commons.mail import SendEmail
from tax_rules.views import CalculateTaxForCart
from commons.product_price import get_price_of_product
from tax_rules.models import TaxRule, GSTState


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


def calculate_tax_for_product_in_order(product_price, quantity, product, order):
    '''
    @param: product_price price of product A/Q to IP
    @param: quantity quantity of product
    @param: product model instance
    @param: order model instance
    '''
    address = order.shipping_address
    # Get the first category of the product
    first_category = product.category.first()

    # TAX CALCULATION
    product_tax = 0
    tax_hsn = set()
    tax_type = ""
    tax_rate = ""
    tax_amount = ""

    if address and address.country == 'India' and address.state:
        # If category exits
        if first_category:

            # get all tax rule for given address(state, country) and category
            taxRules = TaxRule.objects.filter(
                country=address.country,
                state__in=GSTState.objects.filter(name__icontains=address.state),
                category__in=[first_category.id]
            ).distinct()

            # loop through all tax rules
            for taxRule in taxRules:

                # if tax method is not fixed:
                # product tax = quantity * price * rate
                if taxRule.method.lower() == 'percent':
                    category_tax = float(quantity) * float(product_price) * float(taxRule.value / 100)
                else:
                    category_tax = float(taxRule.value)

                # Update hsn, type, rate
                tax_hsn.add(taxRule.display_name)
                tax_type += str(taxRule.gst_type) + '<br>'
                tax_rate += str(taxRule.value) + '%<br>'
                tax_amount += str(format(category_tax, '.2f')) + '<br>'

                product_tax += category_tax
    data = {
        'product_tax': float(product_tax),
        'tax_hsn': list(tax_hsn),
        'tax_type': tax_type,
        'tax_rate': tax_rate,
        'tax_amount': tax_amount
    }
    return data


def calculate_coupon_for_product(product_detail, coupon):
    '''
    @param: product_detail model instance
    @param: coupon model instance
    '''
    product = product_detail.product
    product_price = product_detail.amount
    quantity = product_detail.quantity
    product_discount = 0
    if coupon:
        if {'id': coupon.coupon_category.id} in list(product.category.values('id')):

            # product discount = quantity * price * rate
            if coupon.coupon_method.lower() == 'percent':
                product_discount = float(quantity) * float(product_price) * float(coupon.coupon_value / 100)
            else:
                product_discount = float(coupon.coupon_value)
    return product_discount


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
    order.order_placed = datetime.now()
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
            sendEmail.send((user.email, settings.DEFAULT_EMAIL_TO,))
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
