from datetime import datetime, timedelta
import os
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from category.models import Category
User = get_user_model()


class HomePageView(TemplateView):
    """
    Home page view for Customer
    """
    template_name = 'store/index.html'

    def __init__(self, **kwargs):
        self.context = super(HomePageView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):

        template = ''
        context = self.get_context_data()

        template = "store/index.html"

        return render(request, template_name=template, context=context)

    def get_context_data(self, **kwargs):

        self.context.update({

        })
        return self.context


def send_html_email(to_list, subject, template_name, context, sender, attachments=None):
    """
    Sends html type emails to user.

    """
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html,
                       from_email=sender, to=to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    if attachments:
        for attachment in attachments:
            msg.attach_file(attachment)
    try:
        delivered = msg.send(fail_silently=False)
        if attachments:
            for attachment in attachments:
                os.remove(attachment)
        return delivered
    except Exception as e:
        print("error in email method")
        return 0


def customer_register(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        cnf_password = request.POST['cnf_password']
        if password == cnf_password:
            user = User.objects.filter(email=email)
            print(user, email, user.exists())
            if user.exists():
                messages.add_message(
                    request, messages.WARNING, 'User with this email already exists.')
            else:
                user = User.objects.create_user(email, password)
                context = {
                    'user': user,
                    'domain': request.get_host(),
                    # generate uid
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # generate token
                    'token': account_activation_token.make_token(user),
                    'from': 'punamflutes@gmail.com'
                }
                try:
                    delivered = send_html_email(
                        to_list=[user.email],
                        subject='Email account verfication',
                        template_name='acc_active_email.html',
                        context=context,
                        sender='punamflutes@gmail.com'
                    )
                except Exception as e:
                    print('error while sending email')
                messages.add_message(
                    request, messages.SUCCESS, 'User created successfully. We have sent an email for email verification.')
        else:
            messages.add_message(request, messages.WARNING,
                                 'Password and Confirm Password are not same.')

    return render(request, 'store/register.html', {})


def activate(request, uidb64, token):
    """
    Activates new user.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # to extract UID
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        # user.email_verified = True
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        login(request, user)

        return render(request, 'store/index.html', {'email': user})
    else:
        print('in else')
        # logout(request)
        # return render(request, 'store/index.html', {})


def customer_login(request):
    """
    This is user login method

    Parameters
    request (POST request with user emailid and password.)

    Returns
    Return type
    Redirects the user to their respective dashboard according to their roles defined.

    """
    context = {}
    template = 'store/login.html'
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print('Success')
            return render(request, 'store/index.html', context)
        else:
            messages.add_message(request, messages.WARNING,
                                 'Invalid login credentials.')
            # template = 'store/index.html'
            return render(request, template, context)

    else:
        return render(request, template, context)


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


def wishlist(request):
    context = {}
    template = 'store/wishlist.html'
    return render(request, template, context)


def customer_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('/')
