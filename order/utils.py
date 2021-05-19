from django.conf import settings
from django.urls import reverse
from commons.mail import SendEmail
from commons.SMS import sendSMS


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
    # print(order.status)
    if order.status == 'Canceled' or order.status == 'Shipped' or order.status == 'Delivered':
        # send Email
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

        # send SMS
        try:
            mobile_no = order.shipping_address.mobile_number
            # print(mobile_no)
            if order.status == 'Canceled':
                type = 'order_cancelled'
                # sms = sendSMS(mobile_no, type)
                # sms.send()
            elif order.status == 'Shipped':
                type = 'order_shipped'
                # sms = sendSMS(mobile_no, type)
                # sms.send()
            elif order.status == 'Delivered':
                type = 'order_delivered'
                sms = sendSMS(mobile_no, type)
                sms.send()
        except:
            print('exception in the sending sms..!')
    return message
