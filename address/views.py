from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView, ListView
from django.http import JsonResponse
from django.contrib import messages

from .models import Address
from .forms import AddressCreateForm
from commons.state import IndianStates, IndianUnionTerritories

class CreateAddress(View):
    template_name = 'create_address.html'
    def get(self, request):
        form = AddressCreateForm
        state = (IndianStates + IndianUnionTerritories)
        address_type = request.GET.get('address_type')
        if address_type=="shipping" or address_type=="billing":
            context = {
                'form': form, 
                'state': state, 
                'address_type': address_type,
                'action': 'Add',
            }
            return render(request, self.template_name, context)
        return redirect('customer_profile')

    def post(self, request, *args, **kwargs):
        form = AddressCreateForm(request.POST)
        address_type = request.POST.get('address_type')
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.address_type = address_type
            address.save()

            if address.default:
                update_for_default_address(address)
            return redirect('customer_profile')
        state = (IndianStates + IndianUnionTerritories)
        context = {
            'form': form, 
            'state': state, 
            'address_type': address_type,
            'action': 'Add',
        }
        return render(request, self.template_name, context)


class UpdateAddress(View):
    template_name = 'create_address.html'
    def get(self, request,  *args, **kwargs):
        address_id = kwargs['id']
        address = Address.objects.filter(id=address_id).first()
        if address:
            form = AddressCreateForm(instance=address)
            state = (IndianStates + IndianUnionTerritories)
            address_type = request.GET.get('address_type')
            if address_type=="shipping" or address_type=="billing":
                context = {
                    'form': form, 
                    'state': state, 
                    'address_type': address_type,
                    'action': 'Update',
                }
                return render(request, self.template_name, context)
        return redirect('customer_profile')

    def post(self, request, *args, **kwargs):
        address_id = kwargs['id']
        address = Address.objects.filter(id=address_id).first()
        form = AddressCreateForm(request.POST, instance=address)
        address_type = request.POST.get('address_type')
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.address_type = address_type
            address.save()
            
            if address.default:
                update_for_default_address(address)
            return redirect('customer_profile')
        state = (IndianStates + IndianUnionTerritories)
        context = {
            'form': form, 
            'state': state, 
            'address_type': address_type,
            'action': 'Update',
        }
        return render(request, self.template_name, context)

class SetDefaultAddress(View):
    def get(self, request, *args, **kwargs):
        address_id = kwargs['id']
        address = Address.objects.filter(id=address_id).first()
        if address:
           update_for_default_address(address)
        return redirect('customer_profile')

def update_for_default_address(address):
    '''
    @param address model
    '''
    # Get all user address
    all_user_address = Address.objects.filter(
        user=address.user, address_type=address.address_type
    )

    # make all user default address to false
    for u_address in all_user_address:
        u_address.default = False
        u_address.save()

    # make current address as default
    address.default = True
    address.save()


