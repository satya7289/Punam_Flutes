from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import ValidateCoupon

urlpatterns = [
    path('validate-coupon', login_required(ValidateCoupon.as_view()), name='validateCoupon'),
]