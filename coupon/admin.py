from django.contrib import admin
from .models import Coupon

# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'coupon_name', 'coupon_code', 'coupon_method', 'coupon_value', 'coupon_usage_limit', 'coupon_used', 'coupon_category', 'coupon_valid', 'created_at')
    list_filter = ('coupon_valid', )
    search_fields = ('coupon_name',)


admin.site.register(Coupon, CouponAdmin)
admin.site.site_header = 'Punam Flutes Admin Console'
admin.site.site_title = 'Punam Flutes Admin'
