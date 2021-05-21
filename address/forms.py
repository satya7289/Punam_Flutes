from django import forms
from django.forms import TextInput

from commons.country_currency import country as COUNTRY
from address.models import Address


class AddressCreateForm(forms.ModelForm):
    country = forms.ChoiceField(choices=COUNTRY[1:], required=True)
    default = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
        for field in self.Meta.not_required:
            self.fields[field].required = False

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
