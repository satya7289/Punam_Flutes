from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from PIL import Image
from io import BytesIO

from commons.models import TimeStampedModel

# Create your models here.
TESTIMONIAL_DIR = 'testinomial'
storage = S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME)


class Blog(models.Model):
    display_name = models.CharField(max_length=200)
    menu_item_name = models.CharField(max_length=200)
    sequence = models.IntegerField()
    description = models.TextField()
    TYPE_CHOICES = (
        ('card', 'card'),
        ('carousal', 'carousal'),
        ('banner', 'banner'),
    )
    blog_type = models.CharField(
        choices=TYPE_CHOICES,
        default='card',
        max_length=10
    )
    blog_category = models.OneToOneField(
        'category.Category', on_delete=models.CASCADE)

    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name


class Testimonial(TimeStampedModel):
    image = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=False, null=False, upload_to=TESTIMONIAL_DIR + '/%Y%m%d%M%S')
    alt = models.CharField(max_length=1024, blank=True, null=True)
    name = models.CharField(max_length=2048, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=True, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    def resize_image(self):
        memfile = BytesIO()
        image = Image.open(self.image)
        image_size = image.size
        if image_size[0] != image_size[1]:
            resize = (250, 250)
            resized_image = image.resize(resize)
            resized_image.save(memfile, 'JPEG', quality=95)
            storage.save(self.image.name, memfile)
            memfile.close()
            image.close()

    class Meta:
        ordering = ("order",)
