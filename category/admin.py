from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'display_name', 'description', 'order', 'publish')
    search_fields = ('display_name', 'description')
    list_filter = ('publish',)

admin.site.register(Category, CategoryAdmin)
