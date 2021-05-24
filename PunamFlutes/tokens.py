from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import random


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


account_activation_token = AccountActivationTokenGenerator()
password_reset_token = TokenGenerator()
