from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from cart.models import Cart, ProductQuantity
from customer.models import User
from customer.models import Profile
from product.models import Product
from commons.product_price import get_price_of_product


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
            'orders': product_details,
            'currency': currency
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # form = CheckoutForm(request.POST)
        # if form.is_valid():
        #     cleaned_data = form.cleaned_data

        #     cart.clear(request)

        #     request.session['order_id'] = o.id
        #     return redirect('process_payment')
        return render(request, self.template_name)




def process_payment(request):
    # cart_id = request.session.get('cart_id')
    # order = get_object_or_404(Cart, id=cart_id)
    host = request.get_host()

    # paypal_dict = {
    #     'business': settings.PAYPAL_RECEIVER_EMAIL,
    #     'amount': '%.2f' % order.total_cost().quantize(Decimal('.01')),
    #     'item_name': 'Order {}'.format(order.id),
    #     'invoice': str(order.id),
    #     'currency_code': 'USD',
    #     'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
    #     'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
    #     'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    # }

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '100',
        'item_name': 'Order {}'.format(11),
        'invoice': str(11),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': 'order', 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')
