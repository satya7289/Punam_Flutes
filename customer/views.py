from datetime import datetime, timezone
import requests
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from PunamFlutes.tokens import account_activation_token, generate_random_otp
from commons.country_currency import country as COUNTRY
from commons.state import IndianStates, IndianUnionTerritories
from commons.SMS import sendSMS

from customer.models import Profile, normalize_phone, BlockedDomain, VerifyMobileOTP
from address.models import Address
from commons.mail import SendEmail
from .forms import UserQueryForm

import phonenumbers

User = get_user_model()


class Registration(View):
    template_name = "registration/registration.html"
    message = ""

    def get(self, request):
        mobile_registration = False
        if settings.COUNTRY == 'India':
            mobile_registration = True
        blockedDomains = [bD['domain'] for bD in BlockedDomain.objects.filter(block_status=True).values('domain')]
        context = {
            'blocked_domain': blockedDomains,
            'mobile_registration': mobile_registration
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Recaptcha Validation
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result['success']:
            self.message = "Registration fails, tick the recaptcha"
            messages.add_message(request, messages.WARNING, self.message)
            return redirect('customer_register')

        password = request.POST['password']
        cnf_password = request.POST['cnf_password']
        if password == cnf_password:
            email = request.POST['email']
            user = User.objects.filter(email=email)
            if user.exists():
                self.message = "User with this email already exists."
                messages.add_message(request, messages.WARNING, self.message)
                return render(request, self.template_name)

            # check for blocked domain
            domain = email.split('@')[1]
            blockedDomain = BlockedDomain.objects.filter(domain=domain).first()
            if blockedDomain:
                self.message = "Opps, something went wrong!!!"
                messages.add_message(request, messages.WARNING, self.message)
                return redirect('customer_register')

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
            return render(request, self.template_name)

        self.message = "Password and Confirm Password are not same."
        messages.add_message(request, messages.WARNING, self.message)
        return render(request, self.template_name)


class RegistrationViaPhone(View):
    mobile_registration = False
    if settings.COUNTRY == 'India':
        mobile_registration = True
    template_name = 'registration/registration_phone.html'
    template_name2 = 'registration/verify_otp.html'
    countryCodes = phonenumbers.COUNTRY_CODE_TO_REGION_CODE

    def get(self, request, *args, **kwargs):
        context = {
            'countryCodes': self.countryCodes,
            'mobile_registration': self.mobile_registration
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        password = request.POST['password']
        cnf_password = request.POST['cnf_password']
        country_code = request.POST['country_code']
        phone = request.POST['phone']
        if password == cnf_password:
            user = User.objects.filter(phone=phone)
            if user.exists():
                self.message = "User with this phone already exists."
                messages.add_message(request, messages.WARNING, self.message)
                return redirect('custommer_registration_phone')

            user = User.objects.create_user(
                phone,
                password,
                country_code=country_code
            )
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # gernerate and Send OTP
            otp = generate_random_otp()
            VerifyMobileOTP.objects.create(
                user=user,
                otp=otp,
                otp_created_at=datetime.now()
            )
            sms = sendSMS(phone, 'otp', OTP=otp)
            sms.send()
            return redirect('verify_otp', uidb64=uid)

        self.message = "Password and Confirm Password are not same."
        messages.add_message(request, messages.SUCCESS, self.message)
        return redirect('custommer_registration_phone')


class VerifyOTP(View):
    template_name = 'registration/verify_otp.html'
    message = ''

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs.get('uidb64')))  # to extract UID
            user = User.objects.get(id=uid)
            mobile_number = phonenumbers.parse(user.phone).national_number
        except:
            return redirect('custommer_registration_phone')
        return render(request, self.template_name, {'mobile_number': mobile_number, 'uidb64': kwargs.get('uidb64')})

    def post(self, request, *args, **kwargs):
        self.message = "Invalid OTP. Try again"
        otp = request.POST.get('otp')
        uid = force_text(urlsafe_base64_decode(kwargs.get('uidb64')))  # to extract UID
        user = User.objects.get(id=uid)
        verify_mobile_otp = VerifyMobileOTP.objects.get(user=user)
        if verify_mobile_otp:
            # if today's limit exceed
            if verify_mobile_otp.today_attempts > 5:
                self.message = "Today's limit excced try again tommorow"
                messages.add_message(request, messages.WARNING, self.message)
                return redirect('custommer_registration_phone')

            # if otp is expired
            if (verify_mobile_otp.otp_created_at - datetime.now(timezone.utc)).total_seconds() > (verify_mobile_otp.time_limit * 60):
                self.message = "OTP expires. Click on resend to send another OTP"
                messages.add_message(request, messages.WARNING, self.message)
                return redirect('verify_otp', uidb64=kwargs.get('uidb64'))

            # if otp is matched and otp is valid
            if verify_mobile_otp.otp == otp and verify_mobile_otp.valid:

                # Change the phone verified status to true
                user.phone_verified = True
                user.save()

                # Make OTP invalid
                verify_mobile_otp.valid = False
                verify_mobile_otp.save()

                # Return to the login page
                self.message = "User created successfully. You can login now"
                messages.add_message(request, messages.SUCCESS, self.message)
                return redirect('customer_login')

            verify_mobile_otp.last_attempted_at = datetime.now()
            verify_mobile_otp.save()

        messages.add_message(request, messages.ERROR, self.message)
        return redirect('verify_otp', uidb64=kwargs.get('uidb64'))


def resend_otp(request, *args, **kwargs):
    try:
        otp = generate_random_otp()
        uid = force_text(urlsafe_base64_decode(kwargs.get('uidb64')))  # to extract UID
        user = User.objects.get(id=uid)
        mobile_number = phonenumbers.parse(user.phone).national_number
        verify_mobile_otp = VerifyMobileOTP.objects.get(user=user)

        if verify_mobile_otp.today_attempts > 5:
            # calculate the difference
            days = (verify_mobile_otp.otp_created_at - verify_mobile_otp.last_attempted_at).days
            if days <= 0:
                return JsonResponse({'message': 'fail', 'status': '2'})

            # update the today's attempts and total attempts
            verify_mobile_otp.total_attempts = verify_mobile_otp.today_attempts
            verify_mobile_otp.today_attempts = 0

        # update the otp and save
        verify_mobile_otp.otp = otp
        verify_mobile_otp.today_attempts = verify_mobile_otp.today_attempts + 1
        verify_mobile_otp.otp_created_at = datetime.now()
        verify_mobile_otp.save()

        # Send SMS
        sms = sendSMS(mobile_number, 'otp', OTP=otp)
        sms = sms.send()
        # print(otp)
    except:
        return JsonResponse({'message': 'fail', 'status': '0'})
    return JsonResponse({'message': 'success', 'status': '1'})


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
