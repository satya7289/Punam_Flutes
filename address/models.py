from django.db import models
from django.contrib.auth import get_user_model

from customer.models import User

User = get_user_model()

# Initialize logger.
# logger = logging.getLogger(__name__)

# Create your models here for address.


class Address(models.Model):
    """ 
    Address table for storing customer's address

    Atrributes:
    -----------

    address_id      : AutoField(primary_key)
    street_address  : CharField
    locality        : CharField
    region          : CharField
    postal_code     : CharField
    country         : CharField

    Methods:
    --------

    get_pk(self)
        Returns the primary key of the address object.


    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=1024, null=False, blank=False)
    # Field for City/Town.
    city = models.CharField(max_length=16, null=False, blank=False)
    # Field for State/Province/County.
    state = models.CharField(max_length=16, null=True, blank=True)
    # Field for ZIP/Postal Code.
    postal_code = models.CharField(max_length=16, null=True, blank=True)
    # Field for Country.
    country = models.CharField(max_length=20, null=False, blank=False)

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
