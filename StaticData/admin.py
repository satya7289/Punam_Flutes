from django.contrib import admin
from django.urls import path

from .models import SlideShow

# Register your models here.
class SlideShowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'heading', 'description', 'redirect_link', 'order', 'created_at')
    list_filter = ('publish', )

admin.site.register(SlideShow, SlideShowAdmin)
