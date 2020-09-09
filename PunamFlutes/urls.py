from django.contrib import admin
from django.urls import path, include, re_path
from .views import HomePageView, customer_login, customer_register, customer_logout, activate, cart, checkout, contact, wishlist

urlpatterns = [
    path('flutes_admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='dashboard'),
    path('customer_login/', customer_login, name='customer_login'),
    path('customer_register/', customer_register, name='customer_register'),
    # path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('wishlist/', wishlist, name='wishlist'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
    path('logout/', customer_logout, name='logout'),
    path('product/', include('product.urls')),
    path('cart', include('cart.urls')),
]
