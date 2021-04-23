from commons.ip_detect import set_country_data

class ProductPricingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # set the country to setting based on IP
        set_country_data(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
