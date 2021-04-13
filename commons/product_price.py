from product.models import Product
from django.conf import settings
from commons.ip_detect import request_to_geoplugin, get_ip_detail

def get_price_of_product(request, product, country=None):

    '''
        Logic for getting price of the product.
        1. Get the country of the customer(based on either IP or given country).
        2. Get the actual currency of the country
        3. Find if any country price is mentioned in the product.
            3.1. If yes:
                3.1.1. Get the currency, MRP & Selling Price.
            3.2 if no:
                3.2.1. Get the currency, MRP & Selling Price of ANY country(default country)
        4. Get the calculated selling price based on 2nd step's currency using 3rd step's currency.
        5. Return price, country, currency
    '''
    
    # Get the detail of the IP
    ip_detail = get_ip_detail(request)

    # If not given country get from IP
    if not country:
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

    # TODO: Request currency conversion rate based on the country.
    
    if geoplugin:
        price = float(default.selling_price) * geoplugin['data']['geoplugin_currencyConverter']
        currency = geoplugin['data']['geoplugin_currencySymbol']
        mrp_price = float(default.MRP) * geoplugin['data']['geoplugin_currencyConverter']
    else:
        price = float(default.selling_price) * 73.4442 # default set USD conversion rate
        currency = '$'
        mrp_price = float(default.MRP) * 73.4442
    
    return {'price': format(price,'.2f'), 'MRP':format(mrp_price,'.2f'), 'currency': currency, 'country': country}
