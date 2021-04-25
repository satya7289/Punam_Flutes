from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

from commons.models import TimeStampedModel

SLIDESHOW_DIR = 'slideShow'

STORE_TYPE = [['Indian Stores', 'Indian Stores'], ['International Stores', 'International Stores']]
SUPPORT_TYPE =[['TermsCondition', 'TermsCondition'], ['ReturnPolicy', 'ReturnPolicy'], ['RefundPolicy', 'RefundPolicy']]
STATIC_DATA_CHOICES = [['-----', ''], ['contactUs', 'contactUs'], ['map', 'map']]


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
    
class Store(TimeStampedModel):
    display_name = models.CharField(max_length=1024, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    store_type = models.CharField(max_length=100, choices=STORE_TYPE, null=True, blank=True)
    first_description = models.TextField(blank=True, null=True)
    main_description = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.display_name
    
    class Meta:
        ordering = ('store_type', 'order')


class Support(TimeStampedModel):
    display_name = models.CharField(max_length=1024, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    first_description = models.TextField(blank=True, null=True)
    main_description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=1024, blank=True, null=True)
    publish = models.BooleanField(default=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.display_name    

    class Meta:
        ordering = ('display_name', 'order')
    
class StaticData(TimeStampedModel):
    display_name = models.CharField(max_length=1024)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_2 = models.TextField(blank=True, null=True)
    description_3 = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name
