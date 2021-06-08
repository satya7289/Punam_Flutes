from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

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
    PasswordResetRequest
)

urlpatterns = [
    # login - logout
    path('login/', Login.as_view(), name='customer_login'),
    path('logout/', customer_logout, name='logout'),

    # registeration
    path('register/', Registration.as_view(), name='customer_register'),
    path('register-via-phone/', RegistrationViaPhone.as_view(), name='custommer_registration_phone'),
    path('register-via-phone-?p<uidb64>[0-9A-Za-z_\-]+/verify-otp', VerifyOTP.as_view(), name='verify_otp'),
    path('register-via-phone-?p<uidb64>[0-9A-Za-z_\-]+/resend-otp', resend_otp, name='resend_otp'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),

    # forget password
    path("password_reset", PasswordResetRequest.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgetPassword/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="forgetPassword/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='forgetPassword/password_reset_complete.html'), name='password_reset_complete'),

    # others
    path('profile/', login_required(CustomerProfile.as_view()), name='customer_profile'),
    path('address', login_required(CustomerAddress.as_view()), name='customer_address'),
    path('check-username', CheckUsername.as_view(), name='check_username'),
    path('query', UserQueryView.as_view(), name='customer_query'),
]
