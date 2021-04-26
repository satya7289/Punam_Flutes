import os
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from PunamFlutes.tokens import account_activation_token
from commons.country_currency import country as COUNTRY
from commons.state import IndianStates, IndianUnionTerritories

from customer.models import Profile, normalize_phone
from address.models import Address
from commons.mail import SendEmail
from .forms import UserQueryForm

import phonenumbers

User = get_user_model()


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
        print("error in email method", e)
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
                    send_html_email(
                        to_list=[user.email],
                        subject='Email account verfication',
                        template_name='acc_active_email.html',
                        context=context,
                        sender='punamflutes@gmail.com'
                    )
                except Exception as e:
                    print('error while sending email', e)
                messages.add_message(
                    request, messages.SUCCESS, 'User created successfully. We have sent an email for email verification.')
        else:
            messages.add_message(request, messages.WARNING,
                                 'Password and Confirm Password are not same.')

    return render(request, 'store/register.html', {})


class Registration(View):
    template_name = "store/register.html"
    message = ""
    countryCodes = phonenumbers.COUNTRY_CODE_TO_REGION_CODE

    def get(self, request):
        return render(request, self.template_name, {'countryCodes': self.countryCodes})

    def post(self, request):
        registrationType = request.POST['type']
        password = request.POST['password']
        cnf_password = request.POST['cnf_password']
        if password == cnf_password:
            if registrationType == "email":
                email = request.POST['email']
                user = User.objects.filter(email=email)
                if user.exists():
                    self.message = "User with this email already exists."
                    messages.add_message(request, messages.WARNING, self.message)
                else:
                    email_opt = request.POST.get('email_opt')
                    if email_opt:
                        email_opt = True
                    else:
                        email_opt = False
                    user = User.objects.create_user(email, password)

                    # send account activation code
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    url = request.scheme + "://" + request.get_host() + reverse('activate', kwargs={'uidb64': uid, 'token': token})
                    data = {
                        "link": url
                    }
                    sendEmail = SendEmail('activation.html', data, 'Verify Account')
                    # sendEmail.send(('satyaprakashaman60@gmail.com',))
                    sendEmail.send((user.email,))

                    self.message = "User created successfully. We have sent an email for email verification."
                    messages.add_message(request, messages.SUCCESS, self.message)
            elif registrationType == "phone":
                country_code = request.POST['country_code']
                phone = request.POST['phone']
                user = User.objects.filter(phone=phone)
                if user.exists():
                    self.message = "User with this phone already exists."
                    messages.add_message(request, messages.WARNING, self.message)
                else:
                    user = User.objects.create_user(
                        phone,
                        password,
                        country_code=country_code
                    )
                    print(user)
                    # TODO send account activation code

                    self.message = "User created successfully."
                    messages.add_message(request, messages.SUCCESS, self.message)
        else:
            self.message = "Password and Confirm Password are not same."
            messages.add_message(request, messages.WARNING, self.message)
        return render(request, self.template_name, {'countryCodes': self.countryCodes})


class Login(View):
    template_name = "store/login.html"
    template_name2 = 'store/index.html'
    message = ""
    countryCodes = phonenumbers.COUNTRY_CODE_TO_REGION_CODE

    def get(self, request):
        return render(request, self.template_name, {'countryCodes': self.countryCodes})

    def post(self, request):
        loginType = request.POST['type']
        if loginType == "email":
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return render(request, self.template_name2)
        elif loginType == "phone":
            country_code = request.POST['country_code']
            phone = request.POST['phone']
            phone = normalize_phone(phone, country_code)
            password = request.POST['password']
            user = authenticate(request, username=phone, password=password)
            if user:
                login(request, user)
                return render(request, self.template_name2)

        self.message = "Invalid login credentials."
        messages.add_message(request, messages.WARNING, self.message)
        return render(request, self.template_name)


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
        user.email_verified = True
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        login(request, user)

        return render(request, 'store/index.html', {'email': user})
    else:
        logout(request)
        return redirect('dashboard')


def customer_login(request):
    """

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


def customer_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('/')


class CustomerProfile(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        # Get the logged in user
        user = request.user

        # Get the profile of the user
        profile = Profile.objects.filter(user=user).first()

        # Get all the address of the user
        billing_address = Address.objects.filter(user=user, address_type='billing', default=True).first()
        shipping_address = Address.objects.filter(user=user, address_type='shipping', default=True).first()

        # countries
        country = COUNTRY[1:]
        state = (IndianStates + IndianUnionTerritories)

        if not profile:
            profile = None

        if not billing_address:
            billing_address = None

        if not shipping_address:
            shipping_address = None

        context = {
            'profile': profile,
            'email' : user.email,
            'phone' : user.phone,
            'billing_address' : billing_address,
            'shipping_address': shipping_address,
            'country': country,
            'state': state,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = request.user
        profile = Profile.objects.filter(user=user).first()

        if profile:
            if first_name:
                profile.first_name = first_name
            if last_name:
                profile.last_name = last_name
            profile.save()
            return redirect('dashboard')

        profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name)
        return redirect('customer_profile')


class CustomerAddress(View):
    template_name = 'address.html'

    def get(self, request):

        # Get the logged in user
        user = request.user

        # Get the profile of the user
        profile = Profile.objects.filter(user=user).first()

        address_type = request.GET.get('address_type')

        # Get all the address of the user
        if address_type == "Billing" or address_type == "billing":
            all_address = Address.objects.filter(user=user, address_type='billing').order_by('-default', '-id')
        elif address_type == "Shipping" or address_type == "shipping":
            all_address = Address.objects.filter(user=user, address_type='shipping').order_by('-default', '-id')

        # countries
        country = COUNTRY[1:]
        state = (IndianStates + IndianUnionTerritories)

        if not profile:
            profile = None

        if not all_address:
            all_address = None

        context = {
            'profile': profile,
            'email' : user.email,
            'phone' : user.phone,
            'all_address' : all_address,
            'country': country,
            'state': state,
            'address_type': address_type,
        }
        return render(request, self.template_name, context)


class CheckUsername(View):

    def get(self, request):
        data = {
            'status': '0',
            'message': 'error'
        }
        registrationType = request.GET.get('type')
        if registrationType == "email":
            email = request.GET.get('email')
            user = User.objects.filter(email=email)
            if user.exists():
                data = {
                    'status': '1',
                    'message': 'email exists.'
                }
            else:
                data = {
                    'status': '0',
                    'message': 'email not exists.'
                }
        elif registrationType == "phone":
            phone = request.GET.get('phone')
            country_code = request.GET.get('country_code')
            phone = normalize_phone(phone, country_code)
            user = User.objects.filter(phone=phone)
            if user.exists():
                data = {
                    'status': '1',
                    'message': 'phone exists.'
                }
            else:
                data = {
                    'status': '0',
                    'message': 'phone not exists.'
                }
        return JsonResponse(data)


class SendPhoneOTP(View):
    def get(self, request):
        data = {
            'status': '1',
            'message': 'OTP send'
        }
        return JsonResponse(data)


class UserQueryView(View):
    template_name = 'contact.html'

    def get(self, request):
        form = UserQueryForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserQueryForm(request.POST)
        if form.is_valid():
            form.save()
            form.cleaned_data
            messages.success(request, "We recieved your message.")
            return redirect('customer_query')
        return render(request, self.template_name, {'form': form})
