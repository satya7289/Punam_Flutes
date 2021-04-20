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
from .utils import after_successful_placed_order

class CartView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return render(request, self.template_name, {'cart': None})
        cart = Cart.objects.filter(user=user,is_checkout=False).first()

        if not cart:
            return render(request, self.template_name, {'cart': None})

        product_details = cart.product_detail.all()
        currency = settings.DEFAULT_CURRENCY

        # Add the price and currency according to the user's location to the product
        for product in product_details:
            price_list = get_price_of_product(request,product.product)
            product.price = price_list['price']
            product.currency = price_list['currency']
            currency = price_list['currency']

        context = {
            'cart': cart,
            'products': product_details,
            'currency': currency,
            'range': [i+1 for i in range(10)]
        }
        return render(request, self.template_name, context)


class AddToCart(View):
    def post(self, request, *args, **kwargs):
        '''
        Add products to the user's cart.
        '''
        user = request.user                                                 
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        product = Product.objects.get(id=product_id)
        cart = Cart.objects.filter(user=user,is_checkout=False).first() 

        if cart:
            product_quantity = ProductQuantity.objects.filter(product=product, cart=cart).first()
            if product_quantity:
                product_quantity.quantity = quantity
                product_quantity.save()
            else:
                product_quantity = ProductQuantity.objects.create(product=product, quantity=quantity) 
                cart.product_detail.add(product_quantity)
        else:
            cart = Cart.objects.create(user=user)
            product_quantity = ProductQuantity.objects.create(product=product, quantity=quantity) 
            cart.product_detail.add(product_quantity)

        return redirect('cart')


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        '''
        Remove product from the user's cart.
        '''
        product_id = request.GET.get('product_id')
        cart_id = request.GET.get('cart_id')
        user = request.user                         
        cart = Cart.objects.get(id=cart_id)          
        product = Product.objects.get(id=product_id)                   

        if cart:
            product_detail = ProductQuantity.objects.filter(product=product, cart=cart).first() 
            cart.product_detail.remove(product_detail)
            data = {'message': 'success', 'cart_length': len(cart.product_detail.all())}
            return JsonResponse(data)
            
        data = {'message': 'fail'}
        return JsonResponse(data)
        

class Checkout(View):
    template_name = 'checkout.html'
    continue_template_name = 'continue_checkout.html'

    def get(self, request, *args, **kwargs):

        user = request.user
        profile = Profile.objects.filter(user=user).first()
        user_address = Address.objects.filter(user=user)
        shipping_address = Address.objects.filter(user=user, address_type='shipping')

        # Get the default billing address
        billing_address = Address.objects.filter(user=user, address_type='billing', default=True).first()
        cart = Cart.objects.filter(user=user,is_checkout=False).first()

        product_details = cart.product_detail.all()
        currency = settings.DEFAULT_CURRENCY

        totalPrice = 0
        category_ids = set()

        if request.GET.get('country'):
            # Add the price and currency according to the given country to the product
            country = request.GET.get('country')
            for product in product_details:
                price_list = get_price_of_product(request,product.product)  # TODO: for the country
                product.price = price_list['price']
                product.currency = price_list['currency']
                currency = price_list['currency']
                country = price_list['country']
                totalPrice += float(product.price)

                for category in product.product.category.all():
                    category_ids.add(category.id)
        else:
            # Add the price and currency according to the user's location to the product
            country = settings.DEFAULT_COUNTRY
            for product in product_details:
                price_list = get_price_of_product(request,product.product)
                product.price = price_list['price']
                product.currency = price_list['currency']
                currency = price_list['currency']
                country = price_list['country']
                totalPrice += float(product.price)

                for category in product.product.category.all():
                    category_ids.add(category.id)

        context = {
            'cart': cart,
            'orders': product_details,
            'currency': currency,
            'country': country,
            'profile': profile,
            'user_address': user_address,
            'billing_address': billing_address,
            'shipping_address': shipping_address,
            'email': user.email,
            'phone': user.phone,
            'category_ids': list(category_ids),
            'total_price': totalPrice,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        # Get all the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        shipping_address_id = request.POST.get('shipping_address')
        billing_address_id = request.POST.get('billing_address')
        cart_id = request.POST.get('cart_id')
        total = request.POST.get('total')
        coupon_code = request.POST.get('coupon_code')
        coupon_id = request.POST.get('coupon_id')
        notes = request.POST.get('note')

        # get logged in user and update the profile
        user = request.user
        profile = Profile.objects.get(user=user.id)
        
        if not profile:
            profile = Profile.objects.create(
                user=user,
                first_name=first_name, 
                last_name=last_name, 
                contact_number=contact_number
            )
        else:
            profile.first_name = first_name
            profile.last_name = last_name
            profile.contact_number = contact_number
            profile.save()

        # get the address
        shipping_address = Address.objects.filter(id=shipping_address_id).first()
        billing_address = Address.objects.filter(id=billing_address_id).first()
        cart = Cart.objects.filter(id=cart_id).first()

        # get the coupon
        coupon = Coupon.objects.filter(id=coupon_id)

        if cart and shipping_address and billing_address:
            # get the Order object if already created else create
            order = Order.objects.filter(cart=cart).first()

            if not order:
                order = Order.objects.create(
                    cart=cart, 
                    billing_address=billing_address, 
                    shipping_address=shipping_address,
                    profile=profile, 
                    total=total,
                    status='Pending',
                    notes = notes,
                    coupon = coupon.first() if coupon and coupon.first() else None
                )
            else:
                order.billing_address = billing_address
                order.shipping_address = shipping_address
                order.profile = profile
                order.total = total
                order.notes = notes
                order.coupon =  coupon.first() if coupon and coupon.first() else None
                order.save()

            # Show payment method according to IP
            ip_detail = get_ip_detail(request)
            if ip_detail['message']!='fail':
                country = ip_detail['country']
            else:
                country = settings.DEFAULT_COUNTRY
            
            countryPayment = CountryPayment.objects.filter(country=country).first()
            if not countryPayment:
                countryPayment = CountryPayment.objects.filter(country=settings.DEFAULT_COUNTRY).first()
            
            if countryPayment and (not countryPayment.razorpay) and (not countryPayment.cod):
                all_payment_method_off = True
            else:
                all_payment_method_off = False
            context = {
                'order': order,
                'razorpay': countryPayment.razorpay if countryPayment else '',
                'paypal': countryPayment.paypal if countryPayment else '',
                'cod': countryPayment.cod if countryPayment else '',
                'all_payment_method_off': all_payment_method_off
            }
            return render(request, self.continue_template_name, context)
        return redirect('checkout')


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
                price_list = get_price_of_product(request,product.product)
                product_price = price_list['price']

                # Get the first category of the product
                first_category = product.product.category.first()


                # TAX CALCULATION
                product_tax = 0
                tax_hsn = ""
                tax_type = ""
                tax_rate = ""

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
                                product_tax += float(product.quantity)*float(product_price)*float(taxRule.value/100)
                            else:
                                product_tax += float(taxRule.value)

                            # Update hsn, type, rate
                            tax_hsn += str(taxRule.display_name) + '<br>'
                            tax_type += str(taxRule.gst_type) + '<br>'
                            tax_rate += str(taxRule.value) + '%<br>'

                        # Update the total tax
                        totalTax += product_tax
                    
                # CHECK COUPON APPLIED
                product_discount = 0
                coupon = order.coupon
                if coupon:
                    if {'id': coupon.coupon_category.id} in list(product.product.category.values('id')):
                        
                        # product discount = quantity * price * rate
                        if coupon.coupon_method == 'Percent' or coupon.coupon_method == 'percent':
                            product_discount = float(product.quantity)*float(product_price)*float(coupon.coupon_value/100)
                        else:
                            product_discount = float(coupon.coupon_value)
                        
                        # Update the total tax
                        coupon_total_discount += product_discount
                     

                # Add additional details to products
                product.title = product.product.title
                product.unit_price = product_price
                product.discount = product_discount
                product.qty = product.quantity
                product.net_ammount = float(product_price) * float(product.quantity)
                product.hsn = tax_hsn
                product.tax_rate = tax_rate
                product.tax_type = tax_type
                product.tax_amount = product_tax
                product.total_amount = float(product.net_ammount) +  float(product_tax)  - float(product_discount)

                totalAmount = product.total_amount

            gst_state = GSTState.objects.filter(name__icontains=address.state).first()
            print(gst_state)
            state_code = ""
            if gst_state:
                state_code = gst_state.code
            context = {
                'order_id': order.id,
                'products': products,
                'total_amount': totalAmount,
                'total_tax_amount': totalTax,
                'total_discount': coupon_total_discount,
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
        g = get_ip_detail(request)
        if g['message']=='success':
            currency = g['data']['geoplugin_currencyCode']
        else:
            currency = settings.DEFAULT_CURRENCY
        
        if request.POST.get('razorpay'): # Razorpay
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
            amount = float('%.2f' % order.total)
            if currency=="INR":
                amount *= 100
            resp = client.order.create(dict(
                amount=amount,
                currency=currency,
                receipt=str(order.id)
            ))
            # print(resp)
            if resp['status']=="created":
                payment = Payment.objects.filter(order=order.id).first()

                if payment:
                    if payment.status:  # if payment is done
                        return redirect('dashboard')
                    else:
                        payment.method="razorpay"
                        payment.razorpay=resp['id']
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
                    'callbackurl': scheme  + "://" + host +  reverse('razorpay_done'),
                    'cancelurl': scheme  + "://" + host +  reverse('razorpay_cancel'),
                }
                
                return render(request, 'razorpayRequest.html', context)
            return redirect('checkout')

        elif request.POST.get('paypal'): # Paypal
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
        
        elif request.POST.get('COD'): # COD
            payment = Payment.objects.filter(order=order.id).first()

            if payment:
                if payment.status:  # if payment is done
                    return redirect('dashboard')
                else:
                    payment.method="COD"
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
        razorpayOrder = client.order.fetch(razorpayOrderId)
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
