from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from customer.views import (
    customer_logout,
    CustomerAddress,
    CustomerProfile,
    activate,
    Registration,
    CheckUsername,
    Login,
    UserQueryView,
    RegistrationViaPhone,
    VerifyOTP,
    resend_otp,
)

urlpatterns = [
    path('login/', Login.as_view(), name='customer_login'),
    path('register/', Registration.as_view(), name='customer_register'),
    path('register-via-phone/', RegistrationViaPhone.as_view(), name='custommer_registration_phone'),
    path('register-via-phone-?p<uidb64>[0-9A-Za-z_\-]+/verify-otp', VerifyOTP.as_view(), name='verify_otp'),
    path('register-via-phone-?p<uidb64>[0-9A-Za-z_\-]+/resend-otp', resend_otp, name='resend_otp'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('logout/', customer_logout, name='logout'),
    path('profile/', login_required(CustomerProfile.as_view()), name='customer_profile'),
    path('address', login_required(CustomerAddress.as_view()), name='customer_address'),
    path('check-username', CheckUsername.as_view(), name='check_username'),
    path('query', UserQueryView.as_view(), name='customer_query'),
]
