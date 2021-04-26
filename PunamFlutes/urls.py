from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static

from .views import HomePageView

from .views import (
    contact,
    termsCondition,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='dashboard'),
    path('contact/', contact, name='contact'),
    
    path('flutes_admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('product/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('address/', include('address.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('tax/', include('tax_rules.urls')),
    path('coupon/', include('coupon.urls')),
    path('', include('StaticData.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
