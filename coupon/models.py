from django.db import models

# Create your models here.


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=100)
    coupon_code = models.CharField(max_length=20)
    coupon_value = models.IntegerField(default=0)
    coupon_usage_limit = models.IntegerField(default=0)
    coupon_category = models.ForeignKey(
        'category.Category', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.coupon_name
