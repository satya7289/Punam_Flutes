from django import forms
from django.contrib import admin
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from .models import Product, CountryCurrency, ProductImage

# Register your models here.

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = '__all__'

class CountryCurrencyInLine(admin.TabularInline):
    model = CountryCurrency

class CountryCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'currency', 'MRP', 'selling_price')
    list_filter = ('country', 'currency')

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title', 'search_tags')
    list_display = ('__str__', 'title', 'search_tags', 'Description', 'created_at')
    list_filter = ('category', 'search_tags')
    form = ProductAdminForm
    inlines = [
        CountryCurrencyInLine
    ]

    def Description(self, obj):
        return format_html(obj.description)


admin.site.register(Product, ProductAdmin)
admin.site.register(CountryCurrency, CountryCurrencyAdmin)
admin.site.register(ProductImage)
