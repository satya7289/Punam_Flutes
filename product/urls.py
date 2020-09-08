from .views import product_list, product_detail
from django.urls import path

app_name = 'product'
urlpatterns = [
    path('product_list/<int:id>/', product_list, name='product_list'),
    path('product_detail/<int:id>/', product_detail, name='product_detail'),
]
