from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .views import SyncCurrencyRate

urlpatterns = [
    path('sync-currency-rate', SyncCurrencyRate, name='SyncCurrencyRate'),
]
