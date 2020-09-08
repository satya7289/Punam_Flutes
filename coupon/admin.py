from django.contrib import admin
from .models import Coupon

# Register your models here.
admin.site.register(Coupon)
admin.site.site_header = 'Punam Flutes Admin Console'
admin.site.site_title = 'Punam Flutes Admin'
