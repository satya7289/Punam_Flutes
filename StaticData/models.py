from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

from commons.models import TimeStampedModel

SLIDESHOW_DIR = 'slideShow'

# Create your models here.
class SlideShow(TimeStampedModel):
    image = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=False, null=False,upload_to=SLIDESHOW_DIR +'/%Y%m%d%M%S')
    alt = models.CharField(max_length=1024, blank=True, null=True)
    heading = models.CharField(max_length=1024, blank=True, null=True)
    description = models.CharField(max_length=2048, blank=True, null=True)
    redirect_link = models.CharField(max_length=2048, blank=True, null=True)
    redirect_link_title = models.CharField(max_length=1024, blank=True, null=True)
    publish = models.BooleanField(default=True, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ("order","-created_at")

class CountryCurrencyRate(TimeStampedModel):
    country = models.CharField(max_length=1024, blank=True, null=True)
    alpha_2_code = models.CharField(max_length=20, blank=True, null=True)
    alpha_3_code = models.CharField(max_length=20, blank=True, null=True)
    numeric_code = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=1024, blank=True, null=True)
    currency_code = models.CharField(max_length=20, blank=True, null=True)
    currency_symbol = models.CharField(max_length=100, blank=True, null=True)
    currency_rate = models.FloatField(blank=True, null=True)
    base = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.country
    
    class Meta:
        ordering = ("country",)
