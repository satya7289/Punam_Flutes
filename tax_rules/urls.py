from django.urls import path


# from .views import product_list, product_detail
from .views import CalculateTax, CalculateTaxForCart

urlpatterns = [
    path('calculate-tax', CalculateTax.as_view(), name='calculateTax'),
    path('calculate-order-tax', CalculateTaxForCart, name='calculateTaxForCart'),
]
