from django import forms
from django.contrib import admin

from .models import Blog, Testimonial


class TestimonialAdminForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 10, 'cols': 100}))

    class Meta:
        model = Testimonial
        fields = '__all__'


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'order', 'publish')
    list_filter = ('publish', )
    list_editable = ('order', 'name', 'publish')

    form = TestimonialAdminForm


# Register your models here.
admin.site.register(Blog)
admin.site.register(Testimonial, TestimonialAdmin)
