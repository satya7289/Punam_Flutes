from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

from order.models import Order
from customer.models import User
from commons.mail import SendEmail


class Command(BaseCommand):
    help = 'Get the list of today\'s order'

    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            '--morning',
            action='store_true',
            help='Command for morning',
        )

    def handle(self, *args, **options):
        today = datetime.now()
        if options['morning']:
            confirmed_orders = Order.objects.filter(
                status='Confirmed',
                update_at__time__lte=today.time(),
                update_at__day=today.day - 1,
                update_at__month=today.month,
                update_at__year=today.year
            )
            paid_orders = Order.objects.filter(
                status='Paid',
                update_at__time__lte=today.time(),
                update_at__day=today.day - 1,
                update_at__month=today.month,
                update_at__year=today.year
            )
        else:
            confirmed_orders = Order.objects.filter(
                status='Confirmed',
                update_at__time__lte=today.time(),
                update_at__day=today.day,
                update_at__month=today.month,
                update_at__year=today.year
            )
            paid_orders = Order.objects.filter(
                status='Paid',
                update_at__time__lte=today.time(),
                update_at__day=today.day,
                update_at__month=today.month,
                update_at__year=today.year
            )

        date = today.strftime('%Y-%m-%d')
        # get the admin email
        admin_user = User.objects.filter(admin=True).first()

        if admin_user:
            # send email
            email_template = 'email/total_order.html'
            email_template_subject = f'{date} total orders on flute.in'
            data = {
                'confirmed_orders': len(confirmed_orders),
                'paid_orders': len(paid_orders),
                'link': settings.SITE_URL + '/flutes_admin/order/order/'
            }
            sendEmail = SendEmail(email_template, data, email_template_subject)
            sendEmail.send((admin_user.email,))

        self.stdout.write(self.style.SUCCESS(f'Today\'s {date} total confirmed order {len(confirmed_orders)} & total paid order {len(paid_orders)}'))
