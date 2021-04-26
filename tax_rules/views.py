from django.views.generic import View
from django.http import JsonResponse
import json

from .models import TaxRule, GSTState
from address.models import Address
from cart.models import Cart

from commons.product_price import get_price_of_product

# Create your views here.


class CalculateTax(View):
    # TODO: remove
    '''
    parameter: products, address
    Algorithm:

    if address.country in India:
        taxRule  = where country is India and
                         state is address.state and
                         cateogy is category_ids
        if taxRule.method is percentage
            tax += (taxRule.value/100)*product.price
        else if taxRule.method is fixed
            tax += taxRule.value + product.price
    else:
        taxRule = 0

    '''
    def get(self, request):
        totalTax = 0
        totalPrice = request.GET.get('totalPrice')
        address_id = request.GET.get('address_id')
        category_ids = json.loads(request.GET.get('catgory_ids'))

        if totalPrice and address_id and category_ids:
            address = Address.objects.filter(id=address_id).first()
            if address and address.country == 'India':
                taxRules = TaxRule.objects.filter(
                    country=address.country,
                    state__in=GSTState.objects.filter(name__icontains=address.state),
                    category__in=category_ids
                ).distinct()

                for taxRule in taxRules:
                    if taxRule.method == 'Percent' or taxRule.method == 'percent':
                        totalTax += float(totalPrice) * float(taxRule.value / 100)
                    else:
                        totalTax += float(taxRule.value)

        data = {'totalTax': format(totalTax, '.2f')}
        return JsonResponse(data)


def CalculateTaxForCart(request, cart_id=0, address_id=0):
    totalTax = 0

    # get the cart and the shipping address
    if cart_id != 0 and address_id != 0:
        cart = Cart.objects.filter(id=cart_id).first()
        shipping_address_id = address_id
    else:
        cart = Cart.objects.filter(id=request.GET.get('cart_id')).first()
        shipping_address_id = request.GET.get('shipping_address_id')

    address = Address.objects.filter(id=shipping_address_id).first()

    # if address country is India
    if address and address.country == 'India':

        # Loop over all products in the cart
        for product in cart.product_detail.all():

            # Get the price of product according to IP
            price_list = get_price_of_product(request, product.product)
            product_price = price_list['price']

            # Get the first category of the product
            first_category = product.product.category.first()

            # If category exits
            if first_category:

                # get all tax rule for given address(state, country) and category
                taxRules = TaxRule.objects.filter(
                    country=address.country,
                    state__in=GSTState.objects.filter(name__icontains=address.state),
                    category__in=[first_category.id]
                ).distinct()

                product_tax = 0

                # loop through all tax rules
                for taxRule in taxRules:

                    # if tax method is not fixed:
                    # product tax = quantity * price * rate
                    if taxRule.method == 'Percent' or taxRule.method == 'percent':
                        product_tax += float(product.quantity) * float(product_price) * float(taxRule.value / 100)
                    else:
                        product_tax += float(taxRule.value)
                # Update the total tax
                totalTax += product_tax

    data = {'totalTax': format(totalTax, '.2f')}
    return JsonResponse(data)
