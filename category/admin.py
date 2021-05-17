from django.contrib import admin
from django.utils.html import format_html

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'display_name', 'slug', 'order', 'publish', 'image')
    search_fields = ('display_name', 'slug',)
    list_filter = ('publish',)

    def Image(self, obj):
        url = obj.image.url if obj.image and obj.image.url else ''
        return format_html("<a href='{}'>{}</a>", url, url)


admin.site.register(Category, CategoryAdmin)
