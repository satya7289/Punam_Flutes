import requests
from category.models import Category
from cart.models import Cart

from commons.ip_detect import request_to_geoplugin, get_ip_detail

def extras(request):
    # Get all the categories
    categories = Category.objects.all()

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
        'ip': get_ip_detail(request)
    }
    return context

