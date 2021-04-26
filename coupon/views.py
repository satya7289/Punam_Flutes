from django.views.generic import View
from django.http import JsonResponse

# Create your views here.
from .models import Coupon
from cart.models import Cart
from commons.product_price import get_price_of_product


class ValidateCoupon(View):
    def get(self, request, *args, **kwargs):
        coupon_code = request.GET.get('coupon_code')
        cart = Cart.objects.filter(id=request.GET.get('cart_id')).first()
        coupon = Coupon.objects.filter(coupon_code=coupon_code).first()
        message = 'fail'
        coupon_total_discount = 0
        coupon_id = 0
        if coupon:
            remaining = coupon.coupon_usage_limit - coupon.coupon_used
            if remaining > 0 and coupon.coupon_valid:
                if cart:
                    # Loop over all products in the cart
                    for product in cart.product_detail.all():
                        if {'id': coupon.coupon_category.id} in list(product.product.category.values('id')):

                            # Get the price of product according to IP
                            price_list = get_price_of_product(request, product.product)
                            product_price = price_list['price']

                            # product discount = quantity * price * rate
                            if coupon.coupon_method == 'Percent' or coupon.coupon_method == 'percent':
                                product_discount = float(product.quantity) * float(product_price) * float(coupon.coupon_value / 100)
                            else:
                                product_discount = float(coupon.coupon_value)

                            # Update the total tax
                            coupon_total_discount += product_discount
                    message = 'success'
                    coupon_id = coupon.id
        data = {
            'message': message,
            'coupon_discount': coupon_total_discount,
            'coupon_id': coupon_id,
        }
        return JsonResponse(data)
