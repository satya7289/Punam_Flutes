import requests

def request_to_geoplugin(client_ip, base_currency='USD'):
    if client_ip!='0.0.0.0' and client_ip!='127.0.0.1':
        '''
            Get the Ip detail with country name by using `geoplugin`.
        '''
        geoplugin_url = 'http://www.geoplugin.net/json.gp?ip=' + str(client_ip) + '&base_currency=' + base_currency
        geoplugin = requests.get(geoplugin_url)

        if geoplugin.status_code == 200:
            return {
                'message': 'success',
                'country':geoplugin.json()['geoplugin_countryName'],
                'data':geoplugin.json(),
                'user_ip': client_ip
        }
    return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
