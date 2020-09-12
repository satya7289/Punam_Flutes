from django.contrib import admin
from django.urls import path, include, re_path

from .views import HomePageView, contact, wishlist

urlpatterns = [
    path('', HomePageView.as_view(), name='dashboard'),
    path('contact/', contact, name='contact'),
    path('wishlist/', wishlist, name='wishlist'),

    path('flutes_admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('product/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
