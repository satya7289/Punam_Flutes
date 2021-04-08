from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
import json

from .models import TaxRule, GSTState
from address.models import Address
from category.models import Category

# Create your views here.

class CalculateTax(View):
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
        category_ids= json.loads(request.GET.get('catgory_ids'))
        
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
                        totalTax += float(totalPrice) *float(taxRule.value/100)
                    else:
                        totalTax += float(taxRule.value)
                
        data = {'totalTax': format(totalTax,'.2f')}
        return JsonResponse(data)
