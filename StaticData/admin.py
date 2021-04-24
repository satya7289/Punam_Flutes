from django import forms
from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from django.urls import reverse

from .models import SlideShow, Store, Support, ContactUs, SUPPORT_TYPE

# Register your models here.

class StoreAdminForm(forms.ModelForm):
    first_description = forms.CharField(widget=CKEditorWidget(), required=False)
    main_description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Store
        fields = '__all__'


class SupportAdminForm(forms.ModelForm):
    first_description = forms.CharField(widget=CKEditorWidget(), required=False)
    main_description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Support
        fields = '__all__'


class ContactUsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = ContactUs
        fields = '__all__'

class SlideShowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'heading', 'description', 'redirect_link', 'order', 'created_at')
    list_filter = ('publish', )

class StoreAdmin(admin.ModelAdmin):
    form = StoreAdminForm
    list_display = ('__str__', 'display_name', 'slug', 'store_type', 'publish', 'order', 'preview')
    list_filter = ('publish', 'store_type', )

    def Description(self, obj):
        return format_html(obj.description)
    
    def preview(self, obj):
        if obj.store_type == 'Indian Stores':
            url = reverse('indianStore_detail', kwargs={'slug':obj.slug})
        else:
            url = reverse('internationalStore_detail', kwargs={'slug':obj.slug})
        return format_html("<a href={}>{}</a>", url, 'Preview')

class SupportAdmin(admin.ModelAdmin):
    form = SupportAdminForm
    list_display = ('__str__', 'display_name', 'slug', 'publish', 'order', 'preview')
    list_filter = ('publish', )

    def preview(self, obj):
        url = reverse('support', kwargs={'slug':obj.slug})
        return format_html("<a href={}>{}</a>", url, 'Preview')
    

class ContactUsAdmin(admin.ModelAdmin):
    form = ContactUsAdminForm
    list_display = ('__str__', 'display_name', 'description', 'publish')
    list_filter = ('publish', )

admin.site.register(SlideShow, SlideShowAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Support, SupportAdmin)
# admin.site.register(ContactUs, ContactUsAdmin)
