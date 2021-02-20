from django.urls import path


# from .views import product_list, product_detail
from .views import ProductListView, ProductDetailView

app_name ='product'

urlpatterns = [
    path('<int:category_id>/list/', ProductListView.as_view(), name='product_list'),
    path('<int:category_id>/product-detail/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]
