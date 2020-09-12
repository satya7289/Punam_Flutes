from django.urls import path, re_path

from customer.views import customer_login, customer_register, customer_logout, activate

urlpatterns = [
    path('login/', customer_login, name='customer_login'),
    path('register/', customer_register, name='customer_register'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('logout/', customer_logout, name='logout'),
    # path('profile/', include('customer.urls')),
]