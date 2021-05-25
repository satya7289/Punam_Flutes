from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from cart.models import Cart
from order.models import Order


class OrderList(View):
    paginate_by = 3
    template_name = 'orders.html'

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(
            cart__in=Cart.objects.filter(
                user=user, is_checkout=True
            )
        )
        return self.pagination(orders)

    def pagination(self, orders):
        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        # Build the context that to be returned
        context = {
            'orders': orders
        }
        return render(self.request, self.template_name, context)


class OrderDetail(View):
    template_name = 'order_detail.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        order_id = kwargs.get('order_id')
        if order_id != "":
            order = Order.objects.filter(id=order_id).first()
            if order and order.user == user:

                # Calculate Tax
                # totalTax = json.loads(CalculateTaxForCart(request, order.cart.id, order.shipping_address.id).content)['totalTax']

                # Calculate Coupon

                # Calculate Subtotal

                context = {
                    'order': order,
                    # 'totalTax': totalTax,
                }
                return render(request, self.template_name, context)
        return redirect('orders')


class CancelOrder(View):
    '''
    Cancel Order if order status is Pending/Confirmed/Paid.
    '''
    def get(self, request):
        if request.GET.get('id'):
            order = Order.objects.filter(id=request.GET.get('id')).first()
            if order.status == 'Pending' or order.status == 'Confirmed' or order.status == 'Paid':
                order.status = 'Canceled'
                order.save()
        return redirect('orders')
