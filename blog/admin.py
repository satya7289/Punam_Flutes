from django import forms
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

from .models import Blog, Testimonial
from .models import BLOG_TYPES
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class TestimonialAdminForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 10, 'cols': 100}))

    class Meta:
        model = Testimonial
        fields = '__all__'


class BlogAdminForm(forms.ModelForm):
    blog_title = forms.CharField(required=True)
    blog_type = forms.ChoiceField(choices=BLOG_TYPES, required=True)
    blog_front_content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 100}), required=True)
    blog_content = forms.CharField(widget=CKEditorUploadingWidget(), required=True)

    class Meta:
        model = Blog
        fields = '__all__'


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'order', 'publish')
    list_filter = ('publish', )
    list_editable = ('order', 'name', 'publish')

    form = TestimonialAdminForm


class BlogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'blog_title', 'blog_type', 'order', 'publish', 'slug', 'views', 'Preview')
    list_filter = ('publish', 'blog_type',)
    list_editable = ('publish', 'order',)

    form = BlogAdminForm

    def Preview(self, obj):
        url = reverse('blog_detail', kwargs={'slug': obj.slug})
        return format_html("<a href={}>{}</a>", url, 'Preview')


# Register your models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
