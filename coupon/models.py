from django.db import models

from category.models import Category
from commons.models import TimeStampedModel
# from customer.models import User

# Create your models here.
METHOD_CHOICES = (
    ('percent', 'percent'),
    ('fixed_amount', 'Fixed Amout'),
)


class Coupon(TimeStampedModel):
    coupon_name = models.CharField(max_length=100)
    coupon_code = models.CharField(max_length=20)
    coupon_method = models.CharField(choices=METHOD_CHOICES, default='percent', max_length=20)
    coupon_value = models.PositiveIntegerField(default=0)
    coupon_usage_limit = models.PositiveIntegerField(default=0)
    coupon_used = models.PositiveIntegerField(default=0)
    coupon_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    coupon_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_name


# class CouponUser(TimeStampedModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username
