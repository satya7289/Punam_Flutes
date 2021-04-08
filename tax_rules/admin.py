from django.contrib import admin
from django import forms
from django.utils.html import format_html


from .models import TaxRule, GSTState
from category.models import Category

# Register your models here.

class TaxRuleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_name', 'gst_type', 'description', 'State', 'country', 'method','value', 'Categories')
    list_filter = ('country','method','category')

    def Categories(self, obj):
        toShow = ''
        for cat in obj.category.all():
            toShow += format_html("<p>{}</p>",cat)
        return format_html(toShow)
    
    def State(self, obj):
        toShow = ''
        for i,s in enumerate(obj.state.all()):
            toShow += format_html("<p>{}</p>",s)
            if i>5:
                toShow += format_html("<p>...</p>")
                break
        return format_html(toShow)

class GSTStateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'code')

admin.site.register(TaxRule,TaxRuleAdmin)
admin.site.register(GSTState,GSTStateAdmin)

