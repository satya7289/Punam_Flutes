from django.urls import path, re_path

from customer.views import customer_login
from customer.views import customer_register
from customer.views import customer_logout
from customer.views import activate
from customer.views import CustomerProfile
from customer.views import Registration
from customer.views import CheckUsername
from customer.views import Login

urlpatterns = [
    path('login/', Login.as_view(), name='customer_login'),
    path('register/', Registration.as_view(), name='customer_register'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('logout/', customer_logout, name='logout'),
    path('profile/', CustomerProfile.as_view(), name='customer_profile'),
    path('check-username', CheckUsername.as_view(), name='check_username'),
]