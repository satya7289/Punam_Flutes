from django.contrib import admin
from .models import Product, CountryCurrency, ProductImage

# Register your models here.


class CountryCurrencyInLine(admin.TabularInline):
    model = CountryCurrency


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        CountryCurrencyInLine
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(CountryCurrency)
admin.site.register(ProductImage)
