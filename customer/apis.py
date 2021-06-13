import requests
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
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

from datetime import datetime, timezone

import phonenumbers

User = get_user_model()


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

