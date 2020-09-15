from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import messages

from .models import Address

class CreateAddress(View):
    def post(self, request, *args, **kwargs):
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        user = request.user
        user_add = Address.objects.filter(user=user)
        
        if not user_add:
            user_add = Address.objects.create(user=user, street_address=street_address, city=city, state=state, postal_code=postal_code, country=country)
            data = {'message': 'success'}
            messages.add_message(request, messages.SUCCESS, 'Successfully, address is added.')
            return redirect('customer_profile')
        
        messages.add_message(request, messages.SUCCESS, 'Oops, Something went wrong.')
        return redirect('customer_profile')


class UpdateAddress(View):
    def post(self, request, *args, **kwargs):
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        address_id = request.POST.get('address_id')

        address = Address.objects.get(id=address_id)
        
        if address:
            address.street_address = street_address
            address.city = city
            address.state = state
            address.postal_code = postal_code
            address.country = country
            address.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully, address is updated.')
            return redirect('customer_profile')
        
        messages.add_message(request, messages.SUCCESS, 'Oops, Something went wrong.')
        return redirect('customer_profile')