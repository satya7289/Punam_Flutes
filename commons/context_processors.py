from django.conf import settings

from category.models import Category
from cart.models import Cart
from StaticData.models import Support, StaticData

from commons.product_price import get_price_of_product
from commons.ip_detect import get_ip_detail


def extras(request):
    # Get all the categories
    categories = Category.objects.filter(publish=True)
    support = Support.objects.filter(publish=True)
    contactUsMap = StaticData.objects.filter(display_name='map', publish=True).first()
    contactUsContact = StaticData.objects.filter(display_name='contactUs', publish=True).first()

    try:
        user = request.user

        # Get the number of product in the cart of logged in user
        cart_length = Cart.objects.filter(user=user, is_checkout=False).first().product_detail.count()
    except:
        cart_length = 0

    context = {
        'categories': categories,
        'all_support': support,
        'cart_length': cart_length,
        'ip': get_ip_detail(request),
        # 'categories_product': categories_product,
        'currency_symbol': settings.CURRENCY_SYMBOL,
        'contactUsMap': contactUsMap,
        'contactUsContact': contactUsContact,
        'SITE_KEY': settings.RECAPTCHA_PUBLIC_KEY,
        'SITE_URL': settings.SITE_URL ,
        'mobile_registration': True if settings.COUNTRY == 'India' else False
    }
    return context


def cartDetail(request):
    user = request.user
    if not user.is_authenticated:
        context = {
            'cart_detail': {
                'cart': None,
                'products': None,
                'range': None
            },
            'is_cart_detail': False
        }
        return context
    cart = Cart.objects.filter(user=user, is_checkout=False).first()

    if not cart:
        context = {
            'cart_detail': {
                'cart': None,
                'products': None,
                'range': None
            },
            'is_cart_detail': False
        }
        return context

    product_details = cart.product_detail.all()

    # Add the price and currency according to the user's location to the product
    for product in product_details:
        price_list = get_price_of_product(request, product.product)
        product.price = price_list['price']

    context = {
        'cart_detail': {
            'cart': cart,
            'products': product_details,
            'range': [1, 2, 5, 10],
        },
        'is_cart_detail': True if len(product_details) > 0 else False
    }
    return context
