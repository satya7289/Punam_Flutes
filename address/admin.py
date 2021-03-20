
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import Address
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('__str__','User', 'address_type', 'street_address', 'city', 'state', 'postal_code', 'country')
    list_filter = ('address_type','country','state','city',)
    search_fields = ('address_type', 'street_address', 'city', 'state', 'postal_code', 'country')

    def User(self,obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label,  obj.user._meta.model_name),  args=[obj.user.id] )
        return format_html('<a href="{}">{}</a>', url, obj.user)

admin.site.register(Address, AddressAdmin)
