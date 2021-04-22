from django.contrib import admin
from django.urls import path

from .models import SlideShow, CountryCurrencyRate

# Register your models here.
class SlideShowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'heading', 'description', 'redirect_link', 'order', 'created_at')
    list_filter = ('publish', )

class CountryCurrencyRateAdmin(admin.ModelAdmin):
    change_list_template = 'CountryCurrencyRate/change_list.html'
    search_fields = ('country', 'currency', 'currency_symbol', 'currency_code', 'alpha_2_code', 'alpha_3_code')
    list_display = ('__str__', 'country', 'alpha_2_code', 'alpha_3_code', 'numeric_code', 'currency', 'currency_code', 'currency_symbol', 'currency_rate', 'base', 'update_at')

admin.site.register(SlideShow, SlideShowAdmin)
admin.site.register(CountryCurrencyRate, CountryCurrencyRateAdmin)
