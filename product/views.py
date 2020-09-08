from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, CountryCurrency
from commons.ip_detect import get_ip_location

# Create your views here.


def product_list(request, id):
    products = Product.objects.filter(category__id=id)
    get_ip_location(request)

    context = {'products': products}
    template = 'productList.html'
    return render(request, template, context)


def product_detail(request, id):

    product = Product.objects.get(pk=id)
    context = {'product': product}
    template = 'productDetail.html'
    return render(request, template, context)
