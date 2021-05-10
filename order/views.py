from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from order.models import Order, Payment
from commons.product_price import get_price_of_product
from commons.mail import SendEmail
from tax_rules.models import TaxRule, GSTState
from tax_rules.views import CalculateTaxForCart

from cart.utils import after_successful_placed_order

import json
import razorpay


class OrderInvoice(View):
    template_name = 'order_invoice.html'

    def get(self, request):
        user = request.user
        order_id = request.GET.get('order_id')
        order = Order.objects.filter(id=order_id).first()

        # if order status is dilivered then only invoice will generate
        if (order and order.status == 'Delivered') or user.is_admin:

            # Get the all products
            products = order.cart.product_detail.all()

            address = order.shipping_address

            coupon_total_discount = 0
            totalTax = 0
            totalAmount = 0

            for product in products:
                # Get the price of product according to IP
                price_list = get_price_of_product(request, product.product)
                product_price = price_list['price']

                # Get the first category of the product
                first_category = product.product.category.first()

                # TAX CALCULATION
                product_tax = 0
                tax_hsn = set()
                tax_type = ""
                tax_rate = ""
                tax_amount = ""

                if address and address.country == 'India':
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
                            if taxRule.method == 'Percent' or taxRule.method == 'percent':
                                category_tax = float(product.quantity) * float(product_price) * float(taxRule.value / 100)
                            else:
                                category_tax = float(taxRule.value)

                            # Update hsn, type, rate
                            tax_hsn.add(taxRule.display_name)
                            tax_type += str(taxRule.gst_type) + '<br>'
                            tax_rate += str(taxRule.value) + '%<br>'
                            tax_amount += str(category_tax) + '<br>'

                            product_tax += category_tax

                        # Update the total tax
                        totalTax += product_tax

                # CHECK COUPON APPLIED
                product_discount = 0
                coupon = order.coupon
                if coupon:
                    if {'id': coupon.coupon_category.id} in list(product.product.category.values('id')):

                        # product discount = quantity * price * rate
                        if coupon.coupon_method == 'Percent' or coupon.coupon_method == 'percent':
                            product_discount = float(product.quantity) * float(product_price) * float(coupon.coupon_value / 100)
                        else:
                            product_discount = float(coupon.coupon_value)

                        # Update the total tax
                        coupon_total_discount += product_discount

                # Add additional details to products
                product.title = product.product.title
                product.unit_price = product_price
                product.discount = format(product_discount, '.2f')
                product.qty = product.quantity
                product.net_ammount = format(float(product_price) * float(product.quantity), '.2f')
                product.hsn = '<br>'.join(tax_hsn)
                product.tax_rate = tax_rate
                product.tax_amount = tax_amount
                product.tax_type = tax_type
                product.net_tax_amount = format(product_tax, '.2f')
                product.total_amount = float(format(float(product.net_ammount) + float(product_tax) - float(product_discount), '.2f'))

                totalAmount += product.total_amount

            gst_state = GSTState.objects.filter(name__icontains=address.state).first()
            state_code = ""
            if gst_state:
                state_code = gst_state.code
            context = {
                'order_id': order.id,
                'products': products,
                'total_amount': format(totalAmount, '.2f'),
                'total_tax_amount': format(totalTax, '.2f'),
                'total_discount': format(coupon_total_discount, '.2f'),
                'shipping_address': order.shipping_address,
                'billing_address': order.billing_address,
                'state_code': state_code
            }
            return render(request, self.template_name, context=context)
        return redirect('dashboard')


class OrderList(View):
    def get(self, request):
        template_name = 'orders.html'
        user = request.user
        orders = Order.objects.filter(
            cart__in=Cart.objects.filter(
                user=user, is_checkout=True
            )
        )
        return render(request, template_name, {'orders': orders})


class CancelOrder(View):
    '''
    Cancel Order if order status is Pending/Confirmed/Paid.
    '''
    def get(self, request):
        if request.GET.get('id'):
            order = Order.objects.filter(id=request.GET.get('id')).first()
            if order.status == 'Pending' or order.status == 'Confirmed' or order.status == 'Paid':
                order.status = 'Canceled'
                order.save()
        return redirect('orders')


@login_required
def process_payment(request):
    host = request.get_host()
    scheme = request.scheme
    order_id = request.POST.get('order')
    order = Order.objects.filter(id=order_id).first()

    if order:
        currency = settings.CURRENCY_CODE
        if request.POST.get('razorpay'):
            # Razorpay
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
            amount = float('%.2f' % order.total)
            if currency == "INR":
                amount *= 100
                resp = client.order.create(dict(
                    amount=amount,
                    currency=currency,
                    receipt=str(order.id)
                ))
            else:
                resp = client.order.create(dict(
                    base_amount=amount,
                    currency=currency,
                    receipt=str(order.id)
                ))
            # print(resp)
            if resp['status'] == "created":
                payment = Payment.objects.filter(order=order.id).first()

                if payment:
                    if payment.status:  # if payment is done
                        return redirect('dashboard')
                    else:
                        payment.method = "razorpay"
                        payment.razorpay = resp['id']
                        payment.save()
                else:
                    payment = Payment.objects.create(
                        order=order,
                        method="razorpay",
                        razorpay=resp['id']
                    )

                context = {
                    'order': resp['id'],
                    'key': settings.RAZORPAY_KEY,
                    'callbackurl': scheme + "://" + host + reverse('razorpay_done'),
                    'cancelurl': scheme + "://" + host + reverse('razorpay_cancel'),
                }

                return render(request, 'razorpayRequest.html', context)
            return redirect('checkout')

        elif request.POST.get('paypal'):
            # Paypal
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': '%.2f' % order.total,
                'item_name': 'Order {}'.format(order.id),
                'invoice': str(order.id),
                'currency_code': currency,
                'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
            }

            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'process_payment.html', {'order': 'order', 'form': form})

        elif request.POST.get('COD'):
            # COD
            payment = Payment.objects.filter(order=order.id).first()

            if payment:
                if payment.status:  # if payment is done
                    return redirect('dashboard')
                else:
                    payment.method = "COD"
                    payment.save()
            else:
                payment = Payment.objects.create(
                    order=order,
                    method="COD"
                )

            after_successful_placed_order(request, payment, "Confirmed")
            return redirect('orders')

    messages.add_message(request, messages.SUCCESS, 'Oops, Something went wrong.')
    return redirect('checkout')


def sendInvoice(request, orderId):
    order = Order.objects.filter(id=orderId).first()
    message = "order is not created"
    if order:
        user = order.user

        product_details = order.cart.product_detail.all()

        # Add the price and currency according to the user's location to the product
        for product in product_details:
            price_list = get_price_of_product(request, product.product)
            product.price = price_list['price']

        data = {
            'products': product_details,
            'total': order.total,
            'shipping_address': order.shipping_address,
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


@csrf_exempt
def payment_done(request):
    # add payment id to the order
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


@csrf_exempt
def razorpay_done(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
    razorpayOrderId = request.POST.get('razorpay_order_id')
    # print(request.POST)
    if razorpayOrderId:
        razorpayPayment = client.order.payments(razorpayOrderId)

        if razorpayPayment['items'][0]['status'] == 'captured':
            # Update the payment status
            payment = Payment.objects.filter(razorpay=razorpayOrderId).first()

            if payment:
                payment.status = True
                payment.save()

                after_successful_placed_order(request, payment)
                return redirect('orders')
    return redirect('dashboard')


@csrf_exempt
def razorpay_cancel(request):
    return render(request, 'payment_cancelled.html')
