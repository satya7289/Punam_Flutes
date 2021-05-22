from django.conf import settings
from product.models import CountryCurrencyRate


def get_price_of_product(request, product, country=None, currency_code=None, currency_rate=None):
    ###############
    #  1. get the country & currency code(based on IP or given country)
    #  2. get the product's country currency
    #  3. calculate the currency rate based on given country currency and product country currency
    #  4. calculate price with the given rate
    #############

    price = 0
    mrp_price = 0
    rate = currency_rate

    if country and currency_code:
        Cc = CountryCurrencyRate.objects.filter(
            country__icontains=country,
            currency_code=currency_code,
        ).first()
        if Cc:
            country = Cc.country
            currency_code = Cc.currency_code
        else:
            country = settings.COUNTRY
            currency_code = settings.CURRENCY_CODE
    else:
        country = settings.COUNTRY
        currency_code = settings.CURRENCY_CODE

    # Get the default Any Country currency of the product.
    default = product.countrycurrency_set.filter(country='Any').first()

    # Get the Country currency of the product based on IP.
    country_currency = product.countrycurrency_set.filter(country=country).first()

    if country_currency:
        default = country_currency

    if default:
        if not rate:
            given_countryCurrencyRate = CountryCurrencyRate.objects.filter(
                currency_code=currency_code
            ).first()
            product_countryCurrencyRate = CountryCurrencyRate.objects.filter(
                currency_code=default.currency
            ).first()

            # if both countryCurrencyRate is known then calculate rate
            # Rate = country currency rate/ product country currency rate
            if given_countryCurrencyRate and product_countryCurrencyRate:
                rate = given_countryCurrencyRate.currency_rate / product_countryCurrencyRate.currency_rate
            else:
                rate = 1

        price = float(default.selling_price) * rate
        mrp_price = float(default.MRP) * rate

    to_return = {
        'price': format(price, '.2f'),
        'MRP': format(mrp_price, '.2f')
    }
    return to_return
