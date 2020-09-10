from django.shortcuts import render
from django.views.generic import View

from cart.models import Cart
from customer.models import User
from customer.models import Profile
from product.models import Product


class CartView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            'cart':Cart.objects.filter(user=user,is_checkout=False).first()
        }
        return render(request, self.template_name, context)


class AddToCart(View):
    template_name = 'cart.html'

    def post(self, request, *args, **kwargs):
        '''
        Add products to the user's cart.
        '''
        user = request.user                                                 # Get the logged in user.
        product = Product.objects.get(id=request.POST.get('product_id'))    # Get the product
        cart = Cart.objects.filter(user=user,is_checkout=False).first()     # Get the user's cart(which has not been checked in).

        if cart:
            cart.product.add(product)
        else:
            cart = Cart.objects.create(user=user)
            cart.product.add(product)

        context = {
            'cart': Cart.objects.filter(user=user,is_checkout=False).first()
        }
        return render(request, self.template_name, context)
