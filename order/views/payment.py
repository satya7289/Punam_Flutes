from django.shortcuts import render, redirect
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from order.models import Order, Payment

from cart.utils import after_successful_placed_order

import razorpay


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
            # if currency == "INR":
            #     amount *= 100
            amount *= 100
            resp = client.order.create(dict(
                amount=amount,
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

                after_successful_placed_order(request, payment, 'Paid')
                return redirect('orders')
    return redirect('dashboard')


@csrf_exempt
def razorpay_cancel(request):
    return render(request, 'payment_cancelled.html')
