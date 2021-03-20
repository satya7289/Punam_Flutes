from django import forms
from django.contrib import admin
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from .models import Product, CountryCurrency, ProductImage
from category.models import Category

# Register your models here.

class ProductAdminForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['images'].disabled = True
    #     self.fields['images'].widget.can_change_related = False

    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'

class CountryCurrencyInLine(admin.TabularInline):
    model = CountryCurrency
    extra = 2


class ProductImageInLine(admin.TabularInline):
    model = Product.images.through
    extra = 2


class CategoryInLine(admin.TabularInline):
    model = Product.category.through
    extra = 1


class CountryCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'currency', 'MRP', 'selling_price')
    list_filter = ('country', 'currency')

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title', 'search_tags')
    list_display = ('__str__', 'title', 'search_tags', 'Description', 'created_at')
    list_filter = ('category', 'search_tags')
    form = ProductAdminForm
    exclude = ('images', 'category', )
    inlines = [
        CategoryInLine,
        ProductImageInLine,
        CountryCurrencyInLine,
    ]

    def Description(self, obj):
        return format_html(obj.description)


admin.site.register(Product, ProductAdmin)
admin.site.register(CountryCurrency, CountryCurrencyAdmin)
admin.site.register(ProductImage)
