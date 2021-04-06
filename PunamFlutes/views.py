from datetime import datetime, timedelta
import os
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from category.models import Category
User = get_user_model()


class HomePageView(TemplateView):
    """
    Home page view for Customer
    """
    template_name = 'store/index.html'

    def __init__(self, **kwargs):
        self.context = super(HomePageView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):

        template = ''
        context = self.get_context_data()

        template = "store/index.html"

        return render(request, template_name=template, context=context)

    def get_context_data(self, **kwargs):

        self.context.update({

        })
        return self.context


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

def wishlist(request):
    context = {}
    template = 'store/wishlist.html'
    return render(request, template, context)

