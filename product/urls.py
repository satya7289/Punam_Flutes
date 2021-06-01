from django.urls import path


# from .views import product_list, product_detail
from .views import ProductListView, ProductDetailView
from .views import SyncCurrencyRate

# app_name ='product'


urlpatterns = [
    path('<int:category_id>/list/', ProductListView.as_view(), name='product_list'),
    path('<int:category_id>/product-detail/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),

    path('list/<slug:slug>/', ProductListView.as_view(), name='category_product_list'),
    path('list/<slug:slug>/<int:product_id>/<slug:product_slug>', ProductDetailView.as_view(), name='category_product_detail'),

    path('sync-currency-rate', SyncCurrencyRate, name='SyncCurrencyRate'),
]
