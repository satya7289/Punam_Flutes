from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'display_name', 'description', 'order')
    search_fields = ('display_name', 'description')

admin.site.register(Category, CategoryAdmin)
