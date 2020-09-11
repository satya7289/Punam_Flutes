from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView

from product.models import Product, CountryCurrency
from category.models import Category

from commons.ip_detect import get_ip_detail, request_to_geoplugin
from commons.product_price import get_price_of_product


class ProductListView(View):
    template_name = 'productList.html'

    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']

        # Get the category and list of products according to the category
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category__id=category_id)
        
        # Add the price and currency according to the user's location
        for product in products:
            price_list = get_price_of_product(request,product)
            product.price = price_list['price']
            product.currency = price_list['currency']

        # Build the context that to be returned
        context = {
            'products': products,
            'category': category
        }
        return render(request, self.template_name, context)
    
class ProductDetailView(View):
    template_name = 'productDetail.html'

    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        category_id = kwargs['category_id']

        # Get the category and product detail
        category = Category.objects.get(id=category_id)
        product = Product.objects.get(id=product_id)

        # Get the price of the product according to the user's location
        get_price = get_price_of_product(request, product)

        # Build the context that to be returned
        context = {
            'product': product,
            'category': category,
            'price': get_price['price'],
            'currency': get_price['currency']
        }
        return render(request, self.template_name, context)
