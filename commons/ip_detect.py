from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception


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

    return country
