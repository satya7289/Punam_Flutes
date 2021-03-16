from django.contrib import admin
from .models import Address
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'address_type', 'street_address', 'city', 'state', 'postal_code', 'country')
    list_filter = ('address_type','country','state','city',)

admin.site.register(Address, AddressAdmin)
