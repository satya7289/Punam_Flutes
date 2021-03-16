from django.db import models
from django.contrib.auth import get_user_model

from customer.models import User
from commons.models import TimeStampedModel

User = get_user_model()

AddressType = [['billing', 'billing'], ['shipping', 'shipping']]

class Address(TimeStampedModel):
    street_address = models.CharField(max_length=1024, null=False, blank=False)
    city = models.CharField(max_length=16, null=False, blank=False)
    state = models.CharField(max_length=16, null=True, blank=True)
    postal_code = models.CharField(max_length=16, null=True, blank=True)
    country = models.CharField(max_length=20, null=False, blank=False)
    address_type = models.CharField(max_length=100, choices=AddressType, blank=True, null=True, default='')
    default = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        postal_state = (
            '%s %s' % (self.city, self.postal_code)
            if (self.city and self.postal_code) else self.postal_code)
        address_fields = [
            self.street_address.replace('\r\n', ', '), self.state,
            postal_state, str(self.country)]
        populated_address_fields = [
            field for field in address_fields if field]
        return ', '.join(populated_address_fields)

    def get_pk(self):
        return self.pk
    # date when data was created
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    user = models.ForeignKey(
        'customer.User', related_name='addresses', on_delete=models.CASCADE)

    class Meta():
        verbose_name_plural = 'addresses'
        ordering = ("default",)
