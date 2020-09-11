from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView


from product.models import Product, CountryCurrency
from category.models import Category
from commons.ip_detect import get_ip_location
from commons.ip_detect import get_currency_from_ip, get_ip_of_the_customer
from commons.context_processors import get_ip_detail, request_to_geoplugin

class ProductListView(View):
    template_name = 'productList.html'

    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']
        customer_ip = get_ip_of_the_customer(request)

        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category__id=category_id)
        # print(products[0].countrycurrency_set.all())
        
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

        category = Category.objects.get(id=category_id)
        product = Product.objects.get(id=product_id)

        # Get the detail of the IP
        ip_detail = get_ip_detail(request)
        if ip_detail['message']!='fail':
            country = ip_detail['country']
        else:
            country = 'Any'
    
        # Get the default Any Country currency of the product.
        default = product.countrycurrency_set.filter(country='Any').first()

        # Get the Country currency of the product based on IP.
        country_currency = product.countrycurrency_set.filter(country=country).first()

        if country_currency:
            default = country_currency
        
        # Request geoplugin with user ip and base currency of the country.
        geoplugin = request_to_geoplugin(ip_detail['user_ip'], default.currency)

        if geoplugin:
            price = float(default.selling_price) * geoplugin['data']['geoplugin_currencyConverter']
            currency = geoplugin['data']['geoplugin_currencySymbol']
        else:
            price = float(default.selling_price) * 73.4442 # default set USD conversion rate
            currency = '$'

        context = {
            'product': product,
            'category': category,
            'price': format(price,'.2f'),
            'currency': currency
        }
        return render(request, self.template_name, context)

# def product_list(request, id):
#     products = Product.objects.filter(category__id=id)
#     get_ip_location(request)

#     context = {'products': products}
#     template = 'productList.html'
#     return render(request, template, context)


# def product_detail(request, id):

#     product = Product.objects.get(pk=id)
#     context = {'product': product}
#     template = 'productDetail.html'
#     return render(request, template, context)
