from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

from commons.models import TimeStampedModel

CATEGORY_DIR = 'category/'
class Category(TimeStampedModel):
    # image size 540, 560 
    image = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=False, null=False,upload_to=CATEGORY_DIR + '/%Y%m%d%M%S')
    alt = models.CharField(max_length=1024, blank=True, null=True)
    display_name = models.CharField(max_length=200, null=False)
    description = models.TextField()
    order = models.PositiveIntegerField(blank=True, null=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name

    class Meta:
        ordering = ("order","display_name")
