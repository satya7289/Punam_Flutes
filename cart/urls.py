from django.urls import path
from django.views.generic.base import TemplateView
from .views import AddToCart
from .views import CartView


urlpatterns = [
    path('/', CartView.as_view(), name='cart'),
    path('/add_to_cart', AddToCart.as_view(), name='add_to_cart'),
]
