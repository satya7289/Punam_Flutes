from product.models import Product
from django.conf import settings
from commons.ip_detect import request_to_geoplugin, get_ip_detail, GetCurrencyRate

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

    if default:

        # TODO: Build an API for getting country based currency rate;
        getCurrencyRate = GetCurrencyRate(request, ip_detail['user_ip'], default.country)

        if getCurrencyRate:
            price = float(default.selling_price) * getCurrencyRate['currencyConvertRate']
            mrp_price = float(default.MRP) * getCurrencyRate['currencyConvertRate']
            currency = getCurrencyRate['currencySymbol']
        else:
            # Default Indian currency rate
            price = float(default.selling_price)
            mrp_price = float(default.MRP)
            currency = '₹'

    else:
        price = 0
        mrp_price = 0
        currency = '₹'
    
    return {'price': format(price,'.2f'), 'MRP':format(mrp_price,'.2f'), 'currency': currency, 'country': country}
