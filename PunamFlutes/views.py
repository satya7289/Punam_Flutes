from datetime import datetime, timedelta
import os
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

from category.models import Category
from cart.models import Cart
from product.models import Product
from StaticData.models import SlideShow

from commons.product_price import get_price_of_product, get_ip_detail
from commons.ip_detect import request_to_geoplugin, get_ip_detail

User = get_user_model()


class HomePageView(View):
    """
    Home page view for Customer
    """
    template_name = 'store/index.html'

    def get(self, request, *args, **kwargs):     
        # Get the slide shows
        slideshows = SlideShow.objects.filter(
            publish=True,
        )

        # Get the new arrival products
        new_arrival_products = Product.objects.order_by('-id')[:11]
        for product in new_arrival_products:
            price_list = get_price_of_product(request,product)
            product.price = price_list['price']
            product.mrp = price_list['MRP']

        # Get the category images
        category_images = Category.objects.filter(
            image__isnull=False, publish=True
        )[:9]

        context = {
            'new_arrival_products': new_arrival_products,
            'slideshows': slideshows,
            'category_images': category_images,
        }
        return render(request, self.template_name, context)


def cart(request):
    context = {}
    template = 'store/cart.html'
    return render(request, template, context)


def checkout(request):
    context = {}
    template = 'store/checkout.html'
    return render(request, template, context)


def contact(request):
    context = {}
    template = 'store/contact.html'
    return render(request, template, context)

def termsCondition(request):
    context = {}
    template = 'store/terms_and_condition.html'
    return render(request, template, context)

def returnPolicy(request):
    context = {}
    template = 'store/return_policy.html'
    return render(request, template, context)

def refundPolicy(request):
    context = {}
    template = 'store/refund_policy.html'
    return render(request, template, context)

def indianStore(request):
    context = {}
    template = 'store/indian_store.html'
    return render(request, template, context)

def internationalStore(request):
    context = {}
    template = 'store/international_store.html'
    return render(request, template, context)

def wishlist(request):
    context = {}
    template = 'store/wishlist.html'
    return render(request, template, context)

