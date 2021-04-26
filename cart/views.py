from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.http import JsonResponse


from order.models import Order
from coupon.models import Coupon
from product.models import Product
from address.models import Address
from StaticData.models import CountryPayment
from cart.models import Cart, ProductQuantity


from address.views import update_for_default_address
from commons.product_price import get_price_of_product
from commons.ip_detect import get_ip_detail
from cart.utils import get_order, is_cart_availabe, get_cart
from address.forms import AddressCreateForm
from commons.state import IndianStates, IndianUnionTerritories


class CartView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return render(request, self.template_name, {'cart': None})
        cart = Cart.objects.filter(user=user, is_checkout=False).first()

        if not cart:
            return render(request, self.template_name, {'cart': None})

        product_details = cart.product_detail.all()

        # Add the price and currency according to the user's location to the product
        for product in product_details:
            price_list = get_price_of_product(request, product.product)
            product.price = price_list['price']

        context = {
            'cart': cart,
            'products': product_details,
            'range': [i + 1 for i in range(10)]
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
        cart = Cart.objects.filter(user=user, is_checkout=False).first()

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
        cart = Cart.objects.get(id=cart_id)
        product = Product.objects.get(id=product_id)

        if cart:
            product_detail = ProductQuantity.objects.filter(product=product, cart=cart).first()
            cart.product_detail.remove(product_detail)
            data = {'message': 'success', 'cart_length': len(cart.product_detail.all())}
            return JsonResponse(data)

        data = {'message': 'fail'}
        return JsonResponse(data)


class ProcessToCheckout(View):

    def get(self, request):
        # get the logged in user
        user = request.user
        if is_cart_availabe(user):
            order = get_order(user)
            if not order:
                order = Order.objects.create(
                    cart=get_cart(user),
                    status='Pending',
                    user=user,
                )
            return redirect('choose_shipping_address')
        return redirect('dashboard')


class ChooseShippingAddress(View):
    template_name = 'choose_shipping_address.html'
    address_type = 'shipping'

    def get(self, request):

        # address creation form
        form = AddressCreateForm
        state = (IndianStates + IndianUnionTerritories)
        all_shipping_address = Address.objects.filter(
            user=request.user,
            address_type=self.address_type
        ).order_by('-default', '-id')
        context = {
            'form': form,
            'state': state,
            'address_type': self.address_type,
            'all_shipping_address': all_shipping_address
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AddressCreateForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.address_type = self.address_type
            address.save()

            if address.default:
                update_for_default_address(address)

            # checks for cart and order
            if not is_cart_availabe(request.user):
                return redirect('dashboard')
            order = get_order(request.user)
            if not order:
                return redirect('dashboard')
            # update the shipping address
            order.shipping_address = address
            order.save()

            return redirect('choose_billing_address')
        state = (IndianStates + IndianUnionTerritories)
        context = {
            'form': form,
            'state': state,
            'address_type': self.address_type,
        }
        return render(request, self.template_name, context)


class ChooseBillingAddress(View):
    template_name = 'choose_billing_address.html'
    address_type = 'billing'

    def get(self, request):
        # get the shipping_address_id if pass
        shipping_address_id = request.GET.get('shipping_address_id')

        # get the logged in user
        user = request.user
        if not is_cart_availabe(user):
            return redirect('dashboard')

        order = get_order(user)
        if not order:
            return redirect('dashboard')

        if shipping_address_id and shipping_address_id != "":
            shipping_address = Address.objects.filter(id=shipping_address_id).first()

            # If shipping address not choosed
            if shipping_address:
                # Update the shipping address
                order.shipping_address = shipping_address
                order.save()

        # address creation form
        form = AddressCreateForm
        state = (IndianStates + IndianUnionTerritories)
        all_billing_address = Address.objects.filter(
            user=request.user,
            address_type=self.address_type
        ).order_by('-default', '-id')
        context = {
            'form': form,
            'state': state,
            'address_type': self.address_type,
            'all_billing_address': all_billing_address
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AddressCreateForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.address_type = self.address_type
            address.save()

            if address.default:
                update_for_default_address(address)

            # checks for cart and order
            if not is_cart_availabe(request.user):
                return redirect('dashboard')
            order = get_order(request.user)
            if not order:
                return redirect('dashboard')
            # update the shipping address
            order.billing_address = address
            order.save()

            return redirect('checkout')
        state = (IndianStates + IndianUnionTerritories)
        context = {
            'form': form,
            'state': state,
            'address_type': self.address_type,
        }
        return render(request, self.template_name, context)


class Checkout(View):
    template_name = 'checkout.html'
    continue_template_name = 'continue_checkout.html'

    def get(self, request, *args, **kwargs):
        # get the logged in user
        user = request.user

        # checks for cart and order
        if not is_cart_availabe(user):
            return redirect('dashboard')
        order = get_order(user)
        if not order:
            return redirect('dashboard')

        # get the shipping_address if pass
        shipping_address_id = request.GET.get('shipping_address_id')
        if shipping_address_id and shipping_address_id != "":
            shipping_address = Address.objects.filter(id=shipping_address_id).first()

            # If shipping address not choosed
            if shipping_address:
                # Update the shipping address
                order.shipping_address = shipping_address
                order.save()

        # if order has not shipping addres; get the default one
        if not order.shipping_address:
            shipping_address = Address.objects.filter(
                user=user,
                address_type='shipping',
                default=True
            ).first()

            # if default shipping address exits
            if shipping_address:
                order.shipping_address = shipping_address
                order.save()
            else:
                return redirect('choose_shipping_address')

        # if order has not billing address; get the default one
        if not order.billing_address:
            billing_address = Address.objects.filter(
                user=user,
                address_type='billing',
                default=True
            ).first()

            # if billing address exits
            if billing_address:
                order.billing_address = billing_address
                order.save()
            else:
                # create a billing address for that user
                billing_address = Address.objects.create(
                    user=user,
                    address_type='billing',
                    full_name=order.shipping_address.full_name,
                    mobile_number=order.shipping_address.mobile_number,
                    postal_code=order.shipping_address.postal_code,
                    street_address=order.shipping_address.street_address,
                    landmark=order.shipping_address.landmark,
                    city=order.shipping_address.city,
                    state=order.shipping_address.state,
                    country=order.shipping_address.country,
                    default=True,
                )
                order.billing_address = billing_address
                order.save()

        cart = order.cart

        product_details = cart.product_detail.all()

        totalPrice = 0

        if request.GET.get('country'):
            # Add the price and currency according to the given country to the product
            country = request.GET.get('country')
            for product in product_details:
                price_list = get_price_of_product(request, product.product)  # TODO: for the country
                product.price = price_list['price']
                totalPrice += float(product.price)
        else:
            # Add the price and currency according to the user's location to the product
            country = settings.COUNTRY
            for product in product_details:
                price_list = get_price_of_product(request, product.product)
                product.price = price_list['price']
                totalPrice += float(product.price)

        context = {
            'cart': cart,
            'orders': product_details,
            'country': country,
            'order': order,
            'total_price': totalPrice,
            'billing_address': order.billing_address,
            'shipping_address': order.shipping_address,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        total = request.POST.get('total')
        coupon_id = request.POST.get('coupon_id')
        customization_request = request.POST.get('customization_request')

        # Get the logged in user
        user = request.user

        # checks for cart and order
        if not is_cart_availabe(user):
            return redirect('dashboard')
        order = get_order(user)
        if not order or (order.id != int(order_id)):
            return redirect('checkout')

        # get the coupon
        coupon = Coupon.objects.filter(id=coupon_id)

        # update the order's data
        order.total = total
        order.customization_request = customization_request
        order.coupon = coupon.first() if coupon and coupon.first() else None
        order.save()

        # Show payment method according to IP
        ip_detail = get_ip_detail(request)
        if ip_detail['message'] != 'fail':
            country = ip_detail['country']
        else:
            country = settings.COUNTRY

        countryPayment = CountryPayment.objects.filter(country=country).first()
        if not countryPayment:
            countryPayment = CountryPayment.objects.filter(country=settings.COUNTRY).first()

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
