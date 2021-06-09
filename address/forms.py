from os import stat
from django import forms
from django.forms import TextInput

from commons.country_currency import country as COUNTRY
from address.models import Address
from product.models import CountryCurrencyRate

class AddressCreateForm(forms.ModelForm):
    countries = CountryCurrencyRate.objects.all().values('country').distinct()
    countries_choice = tuple(map(lambda x: (x['country'], x['country']), countries))
    countries_choice = (('', '-----'),) + countries_choice
    country = forms.ChoiceField(choices=countries_choice, required=True)
    default = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
        for field in self.Meta.not_required:
            self.fields[field].required = False
    
    # def save(self, *args, **kwargs): 
    #     form_ = super().save()
    #     req = kwargs.get('req')
    #     if req:
    #         state = req
    #         print(req, req.get('state'), state, len(state), "satyuayfghj")
    #         if len(state) == 2 and state[0] != '':
    #             form_.state = state[0]
    #             form_.save()
    #         print(args, kwargs)
    #     return form_

    class Meta:
        model = Address
        fields = [
            'full_name',
            'mobile_number',
            'country',
            'state',
            'street_address',
            'landmark',
            'postal_code',
            'city',
            'default',
        ]
        widgets = {
            'full_name': TextInput(attrs={'placeholder': 'Enter full name'}),
            'mobile_number': TextInput(attrs={'placeholder': 'Enter mobile number'}),
            'state': TextInput(attrs={'placeholder': 'Enter State'}),
            'street_address': TextInput(attrs={'placeholder': 'Enter street address'}),
            'landmark': TextInput(attrs={'placeholder': 'Enter landmark'}),
            'postal_code': TextInput(attrs={'placeholder': 'Enter postal code'}),
            'city': TextInput(attrs={'placeholder': 'Enter city'}),
        }
        required = (
            'full_name', 'country', 'street_address', 'postal_code', 'mobile_number'
        )
        not_required = (
            'city', 'state',
        )
