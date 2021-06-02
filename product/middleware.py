from commons.ip_detect import set_country_data, set_site_url


class ProductPricingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        restrict_for_country_data = ['/flutes_admin/', '/blogs/', '/testinomials/']
        # restrict_for_country_data_2 = ['/store', '/support', '/customer']
        # print(request.get_full_path())
        if request.get_full_path() not in restrict_for_country_data:
            # set the country to setting based on IP
            set_country_data(request)

        # set the site url
        set_site_url(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
