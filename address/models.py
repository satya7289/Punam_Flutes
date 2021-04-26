from django.db import models

from commons.models import TimeStampedModel

AddressType = [['billing', 'billing'], ['shipping', 'shipping']]


class Address(TimeStampedModel):
    full_name = models.CharField(max_length=1024, blank=True, null=True)
    mobile_number = models.CharField(max_length=1024, blank=True, null=True)
    postal_code = models.CharField(max_length=64, null=True, blank=True)
    street_address = models.CharField(max_length=1024, null=False, blank=False)
    landmark = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=1024, null=False, blank=False)
    state = models.CharField(max_length=1024, null=True, blank=True)
    country = models.CharField(max_length=1024, null=False, blank=False)
    address_type = models.CharField(max_length=1024, choices=AddressType, blank=True, null=True, default='')
    default = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        full_name = self.full_name if self.full_name else ''
        mobile_number = self.mobile_number if self.mobile_number else ''
        postal_state = (
            '%s %s' % (self.city, self.postal_code)
            if (self.city and self.postal_code) else self.postal_code)
        address_fields = [
            full_name, mobile_number,
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
