import requests
from category.models import Category
from cart.models import Cart


def get_ip_detail(request):
    # Get the IP of the logged in user
    try:              
        user_ip = request.META.get('REMOTE_ADDR')
    except:
        user_ip = '0.0.0.0'

    if user_ip!='0.0.0.0' and user_ip!='127.0.0.1':
        '''
            Get the Ip detail with country name by using `geoplugin`.
        '''
        geoplugin_url = 'http://www.geoplugin.net/json.gp?ip=' + str(user_ip)
        geoplugin = requests.get(geoplugin_url)

        if geoplugin.status_code == 200:
            return {
                'message': 'success',
                'country':geoplugin.json()['geoplugin_countryName'],
                'data':geoplugin.json(),
                'user_ip': user_ip
            }
    return {
        'message':'fail',
        'user_ip':user_ip
    }


def extras(request):

    user = request.user     # Get the logged in user

    # Get all the categories
    categories = Category.objects.all()

    # Get the number of product in the cart of logged in user
    cart_length = Cart.objects.filter(user=user,is_checkout=False).first().product.count()

    context = {
        'categories': categories,
        'cart_length': cart_length,
        'ip': get_ip_detail(request)
    }
    return context

