import requests
from django.conf import settings

from category.models import Category
from cart.models import Cart
from product.models import Product

from commons.product_price import get_price_of_product, get_ip_detail
from commons.ip_detect import request_to_geoplugin, get_ip_detail, set_country_data

def extras(request):
    # Get all the categories
    categories = Category.objects.filter(publish=True)
    
    # # Top 3 categories select 5 products
    # categories_product = []
    # for cat in categories[:3]:
    #     cat_product = cat.product_set.all()[:5]
    #     # for product in cat_
    #     #     price_list = get_price_of_product(request,product)
    #     #     product.price = price_list['price']
    #     #     product.mrp = price_list['MRP']
    #     #     product.currency = price_list['currency']
    #     data = {
    #         'category': cat,
    #         'products': cat_product
    #     }
    #     categories_product.append(data)

    # Get the logged in user
    try:
        user = request.user    

        # Get the number of product in the cart of logged in user
        cart_length = Cart.objects.filter(user=user,is_checkout=False).first().product_detail.count()
    except:
        cart_length = 0

    context = {
        'categories': categories,
        'cart_length': cart_length,
        'ip': get_ip_detail(request),
        # 'categories_product': categories_product,
        'currency_symbol': settings.CURRENCY_SYMBOL
    }
    return context

def cartDetail(request):
    user = request.user
    if not user.is_authenticated:
        context = {
            'cart_detail':{
                'cart': None,
                'products': None,
                'range': None
            },
            'is_cart_detail': False
        }
        return context
    cart = Cart.objects.filter(user=user,is_checkout=False).first()

    if not cart:
        context = {
            'cart_detail':{
                'cart': None,
                'products': None,
                'range': None
            },
            'is_cart_detail': False
        }
        return context

    product_details = cart.product_detail.all()
    currency = settings.CURRENCY_SYMBOL

    # Add the price and currency according to the user's location to the product
    for product in product_details:
        price_list = get_price_of_product(request,product.product)
        product.price = price_list['price']

    context = {
        'cart_detail':{
            'cart': cart,
            'products': product_details,
            'range': [i+1 for i in range(5)]
        },
        'is_cart_detail': True if len(product_details)>0 else False
    }
    return context
