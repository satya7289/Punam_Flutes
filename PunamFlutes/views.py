from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import get_user_model

from category.models import Category
from product.models import Product
from StaticData.models import SlideShow, Store, Support

from commons.product_price import get_price_of_product

User = get_user_model()


class HomePageView(View):
    """
    Home page view for Customer
    """
    template_name = 'store/index.html'

    def get(self, request, *args, **kwargs):
        # Get the slide shows
        slideshows = SlideShow.objects.filter(
            publish=True,
        )

        # Get the new arrival products
        new_arrival_products = Product.objects.order_by('-id')[:11]
        for product in new_arrival_products:
            price_list = get_price_of_product(request, product)
            product.price = price_list['price']
            product.mrp = price_list['MRP']

        # Get the category images
        category_images = Category.objects.filter(
            image__isnull=False, publish=True
        )[:2]

        context = {
            'new_arrival_products': new_arrival_products,
            'slideshows': slideshows,
            'category_images': category_images,
        }
        return render(request, self.template_name, context)


def cart(request):
    context = {}
    template = 'store/cart.html'
    return render(request, template, context)


def checkout(request):
    context = {}
    template = 'store/checkout.html'
    return render(request, template, context)


def contact(request):
    context = {}
    template = 'store/contact.html'
    return render(request, template, context)


def termsCondition(request):
    termsCondition = Support.objects.filter(support_type='Terms&Condition').first()
    context = {
        'termsCondition': termsCondition
    }
    template = 'store/terms_and_condition.html'
    return render(request, template, context)


def returnPolicy(request):
    returnPolicy = Support.objects.filter(support_type='ReturnPolicy').first()
    context = {
        'returnPolicy': returnPolicy
    }
    template = 'store/return_policy.html'
    return render(request, template, context)


def refundPolicy(request):
    refundPolicy = Support.objects.filter(support_type='RefundPolicy').first()
    context = {
        'refundPolicy': refundPolicy
    }
    template = 'store/refund_policy.html'
    return render(request, template, context)


def indianStore(request):
    stores = Store.objects.filter(store_type='Indian Stores')
    context = {
        'stores': stores
    }
    template = 'store/indian_store.html'
    return render(request, template, context)


def internationalStore(request):
    stores = Store.objects.filter(store_type='International Stores')
    context = {
        'stores': stores
    }
    template = 'store/international_store.html'
    return render(request, template, context)


def wishlist(request):
    context = {}
    template = 'store/wishlist.html'
    return render(request, template, context)
