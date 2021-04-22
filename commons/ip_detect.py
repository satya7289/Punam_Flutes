import requests
from django.conf import settings
from product.models import CountryCurrencyRate

def request_to_ip2c(client_ip):
    if client_ip!='0.0.0.0' and client_ip!='127.0.0.1':
        url = 'https://ip2c.org/106.67.4.166'
        req = requests(url)
        req = req.text.split(";")
        country_code_2 = req[1]
        country_code_3 = req[2]
        country = req[3]
    else:
        country = 'India'
        country_code_2 = 'IN'
        country_code_3 = 'IND'
    return country_code_2, country_code_3, country

def set_country_data(request):
    client_ip = get_client_ip(request)
    country_code_2, country_code_3, country =  request_to_ip2c(client_ip)

    countryCurrencyRate = CountryCurrencyRate.objects.filter(
        alpha_2_code=country_code_2,
        alpha_3_code=country_code_3,
        country__icontains=country
    ).first()

    if countryCurrencyRate:
        settings.COUNTRY = countryCurrencyRate.country
        settings.CURRENCY_CODE = countryCurrencyRate.currency_code
        settings.CURRENCY_SYMBOL = countryCurrencyRate.currency_symbol


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def request_to_geoplugin(client_ip, base_currency='USD'):
    # if client_ip!='0.0.0.0' and client_ip!='127.0.0.1':
    #     '''
    #         Get the Ip detail with country name by using `geoplugin`.
    #     '''
    #     geoplugin_url = 'http://www.geoplugin.net/json.gp?ip=' + str(client_ip) + '&base_currency=' + base_currency
    #     geoplugin = requests.get(geoplugin_url)

    #     if geoplugin.status_code == 200:
    #         return {
    #             'message': 'success',
    #             'country':geoplugin.json()['geoplugin_countryName'],
    #             'data':geoplugin.json(),
    #             'user_ip': client_ip
    #     }
    return None

def get_ip_detail(request):
    # Get the IP of the logged in user
    client_ip = get_client_ip(request)

    ip_detail = request_to_geoplugin(client_ip)
    if ip_detail:
        return ip_detail

    return {
        'message':'fail',
        'user_ip':client_ip
    }
