from product.models import Product
from django.conf import settings
from commons.ip_detect import request_to_geoplugin, get_ip_detail

def get_price_of_product(request, product):
    
    # Get the detail of the IP
    ip_detail = get_ip_detail(request)
    if ip_detail['message']!='fail':
        country = ip_detail['country']
    else:
        country = settings.DEFAULT_COUNTRY
    
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
    
    return {'price': format(price,'.2f'), 'currency': currency}