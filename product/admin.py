from django.contrib import admin
from .models import Product, CountryCurrency, ProductImage

# Register your models here.


class CountryCurrencyInLine(admin.TabularInline):
    model = CountryCurrency

class CountryCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'currency', 'MRP', 'selling_price')
    list_filter = ('country', 'currency')

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title', 'search_tags')
    list_display = ('__str__', 'title', 'search_tags', 'description', 'created_at')
    list_filter = ('category', )
    inlines = [
        CountryCurrencyInLine
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(CountryCurrency, CountryCurrencyAdmin)
admin.site.register(ProductImage)
