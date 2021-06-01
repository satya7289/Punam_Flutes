from django import forms
from django.urls import reverse
from django.utils.text import slugify
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import F

from ckeditor.widgets import CKEditorWidget
from .models import (
    Product,
    CountryCurrency,
    ProductImage,
    Inventory,
    CountryCurrencyRate
)

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


class CountryCurrencyForm(forms.ModelForm):
    currency_code = CountryCurrencyRate.objects.all().values('currency_code').distinct()
    currency_code_choice = tuple(map(lambda x: (x['currency_code'], x['currency_code']), currency_code))
    currency_code_choice = (('', '-----'),) + currency_code_choice
    currency = forms.ChoiceField(choices=currency_code_choice, required=True)

    class Meta:
        model = CountryCurrency
        fields = '__all__'


class CountryCurrencyInLine(admin.TabularInline):
    form = CountryCurrencyForm
    model = CountryCurrency
    extra = 0
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class ProductImageInLine(admin.TabularInline):
    model = Product.images.through
    extra = 1
    min_num = 1


class CategoryInLine(admin.TabularInline):
    model = Product.category.through
    extra = 1
    min_num = 1


class InventoryInline(admin.StackedInline):
    model = Inventory
    can_delete = False
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class CountryCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'currency', 'MRP', 'selling_price')
    list_filter = ('country', 'currency')

def update_slug(modeladmin, request, queryset):
    for product in queryset:
        product.slug = slugify(product.title)
        product.save()

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title', 'search_tags')
    list_display = ('__str__', 'title', 'search_tags', 'publish', 'slug', 'update_at', 'created_at')
    list_filter = ('publish', 'category')
    actions = [update_slug]
    form = ProductAdminForm
    exclude = ('images', 'category', )
    inlines = [
        CategoryInLine,
        ProductImageInLine,
        CountryCurrencyInLine,
        InventoryInline,
    ]


    # def categories(self, obj):
    #     toShow = ''
    #     for cat in obj.category.all():
    #         toShow += format_html("<p>{}</p>", cat)
    #     return format_html(toShow)

    # def Description(self, obj):
    #     return format_html(obj.description)

    # def SellingPrice(self, obj):
    #     toShow = ''
    #     for cc in obj.countrycurrency_set.all():
    #         toShow += format_html("<p><b> {} </b> {} {} </p><br>", cc.country, float(cc.selling_price), cc.currency)
    #     return format_html(toShow)


class InventoryAdmin(admin.ModelAdmin):
    search_fields = ('product__title',)
    list_display = ('__str__', 'Product', 'type', 'available', 'sold', 'SellingPrice', 'MRP', 'update_at', 'created_at')
    list_filter = ('type', 'product__category', 'product__publish',)
    list_editable = ('type', 'available')

    def SellingPrice(self, obj):
        toShow = ''
        for cc in obj.product.countrycurrency_set.all():
            toShow += format_html("<p><b> {} </b> {} {} </p><br>", cc.country, float(cc.selling_price), cc.currency)
        return format_html(toShow)

    def MRP(self, obj):
        toShow = ''
        for cc in obj.product.countrycurrency_set.all():
            toShow += format_html("<p><b> {} </b> {} {} </p><br>", cc.country, float(cc.MRP), cc.currency)
        return format_html(toShow)

    def Product(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.product._meta.app_label, obj.product._meta.model_name), args=[obj.product.id])
        return format_html('<a href="{}">{} </a>', url, obj.product)


class CountryCurrencyRateAdmin(admin.ModelAdmin):
    change_list_template = 'CountryCurrencyRate/change_list.html'
    search_fields = ('country', 'currency_symbol', 'currency_code', 'alpha_2_code', 'alpha_3_code')
    list_display = ('__str__', 'country', 'alpha_2_code', 'alpha_3_code', 'numeric_code', 'currency_code', 'currency_symbol', 'currency_rate', 'base', 'update_at')


admin.site.register(Product, ProductAdmin)
admin.site.register(CountryCurrency, CountryCurrencyAdmin)
admin.site.register(ProductImage)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(CountryCurrencyRate, CountryCurrencyRateAdmin)
