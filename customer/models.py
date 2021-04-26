from django.db import models
from django.core import validators
from commons.models import TimeStampedModel
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager)
from django.utils.translation import ugettext_lazy as _

import phonenumbers


def normalize_phone(phone, country_code=None):
    phone = phone.strip().lower()
    phone_number = phonenumbers.parse(phone, country_code)
    phone = phonenumbers.format_number(
        phone_number, phonenumbers.PhoneNumberFormat.E164)
    return phone


class UserManager(BaseUserManager):

    def _create_user(self, email_or_phone, password, **extra_fields):
        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            email_or_phone = self.normalize_email(email_or_phone)
            username, email, phone = (email_or_phone, email_or_phone, "")
        else:
            email_or_phone = normalize_phone(
                email_or_phone, country_code=extra_fields.get("country_code"))
            username, email, phone = (email_or_phone, "", email_or_phone)

        user = self.model(
            username=username,
            email=email,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        user = self._create_user(username, password, **extra_fields)
        print(user)
        return user

    def create_staffuser(self, username, password=None, **extra_fields):
        user = self._create_user(username, password, **extra_fields)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self._create_user(username, password, **extra_fields)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        _('email or phone'), max_length=255, unique=True, db_index=True,
        help_text=_('Required. 255 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[validators.RegexValidator(
            r'^[\w.@+-]+$', _(
                'Enter a valid username. '
                'This value may contain only letters, numbers '
                'and @/./+/-/_ characters.'
            ), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    email = models.EmailField(_('email'), max_length=254, blank=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False, null=False)
    phone_verified = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email_opt_in = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name


class UserQuery(TimeStampedModel):
    full_name = models.CharField(max_length=512, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    contact_number = models.CharField(max_length=512, null=True, blank=True)
    country = models.CharField(max_length=512, null=True, blank=True)
    subject = models.CharField(max_length=512, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name
