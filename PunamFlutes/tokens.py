from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import random
import pyotp
import base64


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.email_verified)
        )


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


def generate_random_otp():
    otp = random.randint(111111, 999999)
    return otp


def generate_totp(user_id, interval=2):
    secret_key = base64.b32encode(str(user_id).encode())
    min = interval * 60
    totp = pyotp.TOTP(secret_key, interval=min)
    return totp.now()


account_activation_token = AccountActivationTokenGenerator()
password_reset_token = TokenGenerator()
