from django.shortcuts import render, redirect
from django.views.generic import View

from .models import SUPPORT_TYPE, Support, Store

# Create your views here.
def indianStore(request):
    stores = Store.objects.filter(store_type='Indian Stores')
    context = {
        'stores': stores
    }
    template = 'store/indian_store.html'
    return render(request, template, context)

def internationalStore(request):
    stores = Store.objects.filter(store_type='International Stores')
    context = {
        'stores': stores
    }
    template = 'store/international_store.html'
    return render(request, template, context)

class SupportView(View):
    template_name = 'support.html'
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        support = Support.objects.filter(slug=slug).first()
        if support:
            return render(request, self.template_name, {'support':support})
        return redirect('dashboard')

class indianStoreDetail(View):
    template_name = 'store_detail.html'
    store_type = 'Indian Stores'
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        store_detail = Store.objects.filter(slug=slug, store_type=self.store_type).first()
        if store_detail:
            return render(request, self.template_name, {'store_detail':store_detail})
        return redirect('indianStore')

class internationalStoreDetail(View):
    template_name = 'store_detail.html'
    store_type = 'International Stores'
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        store_detail = Store.objects.filter(slug=slug, store_type=self.store_type).first()
        if store_detail:
            return render(request, self.template_name, {'store_detail':store_detail})
        return redirect('internationalStore')
