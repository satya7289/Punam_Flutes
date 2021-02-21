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

from cart.models import Cart, ProductQuantity, Order
from customer.models import User
from customer.models import Profile
from product.models import Product
from commons.product_price import get_price_of_product, get_ip_detail
from address.models import Address


class CartView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user,is_checkout=False).first()

        product_details = cart.product_detail.all()
        currency = '$'

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
            data = {'message': 'success'}
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
        cart = Cart.objects.filter(user=user,is_checkout=False).first()

        product_details = cart.product_detail.all()
        currency = '$'

        # Add the price and currency according to the user's location to the product
        for product in product_details:
            price_list = get_price_of_product(request,product.product)
            product.price = price_list['price']
            product.currency = price_list['currency']
            currency = price_list['currency']

        context = {
            'cart': cart,
            'orders': product_details,
            'currency': currency,
            'profile': profile,
            'user_address': user_address,
            'email': user.email
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        # Get all the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')

        address_id = request.POST.get('address')
        cart_id = request.POST.get('cart_id')

        total = request.POST.get('total')

        # get logged in user and update the profile
        user = request.user
        profile = Profile.objects.get(user=user.id)
        
        if not profile:
            profile = Profile.objects.create(user=user,first_name=first_name, last_name=last_name, contact_number=contact_number)
        else:
            profile.first_name = first_name
            profile.last_name = last_name
            profile.contact_number = contact_number

        # get the cart, address
        cart = Cart.objects.get(id=cart_id)
        address = Address.objects.get(id=address_id)

        if cart and address:
            # get the Order object if already created else create
            order = Order.objects.filter(cart=cart).first()

            if not order:
                order = Order.objects.create(cart=cart, address=address, profile=profile, total=total)
            else:
                order.address = address
                order.profile = profile
                order.total = total
                order.save()

            context = {'order': order}
            return render(request, self.continue_template_name, context)
        return redirect('checkout')




def process_payment(request):
    host = request.get_host()
    order_id = request.POST.get('order')
    order = get_object_or_404(Order, id=order_id)

    if order:
        g = get_ip_detail(request)
        if g['message']=='success':
            currency = g['data']['geoplugin_currencyCode']
        else:
            currency = 'USD'
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

    messages.add_message(request, messages.SUCCESS, 'Oops, Something went wrong.')
    return redirect('checkout')

@csrf_exempt
def payment_done(request):
    print(request)
    # add payment id to the order
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')
