import requests

def get_ip_of_the_customer(request):
    try:
        ip = request.META.get('REMOTE_ADDR')
    except:
        ip = '0.0.0.0'
    return ip

def get_currency_from_ip(ip):
    if ip!='0.0.0.0' and ip!='127.0.0.1':
        headers = {'accept': 'application/json'}
        geoplugin_url = 'http://www.geoplugin.net/json.gp?ip=' + str(ip)
        geoplugin = requests.get(geoplugin_url)

        if geoplugin.status_code == 200:
            return {
                'message': 'success',
                'country':geoplugin.json()['geoplugin_countryName'],
                'currency': geoplugin.json()['geoplugin_currencyCode'],

            }
    return {'country': 'Any', 'message': 'fail'}


def get_ip_location(request):
    country = "india"
    # try:
    #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if x_forwarded_for:
    #         ip = x_forwarded_for.split(',')[0]
    #     else:
    #         ip = request.META.get('REMOTE_ADDR')
    #     print(ip)
    #     g = GeoIP2()
    #     loc = g.country('ip')
    #     country = loc['country_name']
    # except Exception as e:
    #     print('Unable to find Ip', e)
    print("DFg")
    return country
