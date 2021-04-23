import requests, json
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from django.conf import settings

from product.models import Product, CountryCurrency, CountryCurrencyRate
from category.models import Category

from commons.ip_detect import get_ip_detail, request_to_geoplugin
from commons.product_price import get_price_of_product


class ProductListView(View):
    template_name = 'productList.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']

        # Get the category and list of products according to the category
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category__id=category_id, publish=True)

        return self.pagination(products, category)
    
    def pagination(self, products, category):
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        
        # Add the price and currency according to the user's location
        for product in products:
            price_list = get_price_of_product(self.request,product)
            product.price = price_list['price']
            product.mrp = price_list['MRP']
        
        # Build the context that to be returned
        context = {
            'products': products,
            'category': category,
            'range': [i+1 for i in range(5)],
        }
        return render(self.request, self.template_name, context)
        
    
class ProductDetailView(View):
    template_name = 'productDetail.html'

    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        category_id = kwargs['category_id']

        # Get the category and product detail
        category = Category.objects.get(id=category_id)
        product = Product.objects.get(id=product_id, publish=True)

        # Get the price of the product according to the user's location
        get_price = get_price_of_product(request, product)

        # Build the context that to be returned
        context = {
            'product': product,
            'category': category,
            'price': get_price['price'],
            'mrp': get_price['MRP'],
            'currency': settings.CURRENCY_SYMBOL,
            'range': [i+1 for i in range(5)]
        }
        return render(request, self.template_name, context)


@staff_member_required
def SyncCurrencyRate(request):
    # Update currency rate using fixer API
    if settings.FIXER_API_KEY and settings.FIXER_API_KEY !='':
        url = 'http://data.fixer.io/api/latest?access_key='+settings.FIXER_API_KEY
        req = requests.get(url)
        if req.status_code == 200 and req.json().get('rates'):
            for currency_code in req.json().get('rates'):
                currency_rate = req.json().get('rates')[currency_code]
                countryCurrencyRate = CountryCurrencyRate.objects.filter(
                    currency_code=currency_code
                ).update(currency_rate=currency_rate, update_at=timezone.now())
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

