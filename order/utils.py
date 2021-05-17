from django.conf import settings
from django.urls import reverse
from commons.mail import SendEmail


def orderStatusChangeNotification(order):
    # send notification if status is
    # Dispatch, Shipped, Delivered, Canceled, Refunded

    email_templates = {
        'Dispatch': 'email/order_dispatch.html',
        'Shipped': 'email/order_shipped.html',
        'Delivered': 'email/order_delivered.html',
        'Canceled': 'email/order_cancel.html',
        'Refunded': 'email/order_refunded.html',
    }

    email_templates_subject = {
        'Dispatch': 'Your order has been dispatched',
        'Shipped': 'Your order has been shipped',
        'Delivered': 'Your order has been delivered',
        'Canceled': 'Your order has been cancelled',
        'Refunded': 'Your order\'s has been refunded',
    }
    print(order.status)
    if order.status == 'Canceled' or order.status == 'Shipped' or order.status == 'Delivered':
        email_template = email_templates[order.status]
        email_template_subject = email_templates_subject[order.status]
        data = {
            'link': settings.SITE_URL + reverse('orders')
        }
        if order.cart.user.email and order.cart.user.email_verified:
            sendEmail = SendEmail(email_template, data, email_template_subject)
            sendEmail.send((order.cart.user.email,))
            message = "mail for order " + order.status + " has been send"
        else:
            message = "either email is not there or email not verified."
        print(message)
        return message
