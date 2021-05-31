from django.db import models
from django.utils.text import slugify
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from PIL import Image
from io import BytesIO

from datetime import datetime

from commons.models import TimeStampedModel

# Create your models here.
TESTIMONIAL_DIR = 'testinomial'
storage = S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME)
BLOG_TYPES = [
    ['text', 'text'],
    ['video', 'video'],
    ['product', 'product'],
    ['new_product', 'new_product'],
    ['learning', 'learning'],
    ['beginner_learning', 'beginner_learning'],
    ['intermediate_learning', 'intermediate_learning'],
    ['advance_learning', 'advance_learning'],
]


class Blog(models.Model):
    blog_title = models.CharField(max_length=1024, blank=True, null=True)
    blog_type = models.CharField(max_length=1024, blank=True, null=True)
    tags = models.CharField(max_length=2048, blank=True, null=True)

    blog_front_content = models.TextField(blank=True, null=True)
    blog_content = models.TextField(blank=True, null=True)

    image1 = models.ImageField(storage=storage, blank=True, null=True, upload_to='blogsImages/%Y%m%d%M%S')
    image2 = models.ImageField(storage=storage, blank=True, null=True, upload_to='blogsImages/%Y%m%d%M%S')
    image3 = models.ImageField(storage=storage, blank=True, null=True, upload_to='blogsImages/%Y%m%d%M%S')
    image4 = models.ImageField(storage=storage, blank=True, null=True, upload_to='blogsImages/%Y%m%d%M%S')

    video1 = models.URLField(max_length=1024, blank=True, null=True)
    video2 = models.URLField(max_length=1024, blank=True, null=True)
    video3 = models.URLField(max_length=1024, blank=True, null=True)
    video4 = models.URLField(max_length=1024, blank=True, null=True)

    order = models.PositiveIntegerField(blank=True, null=True)
    publish = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=1024)

    views = models.PositiveIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        if not self.slug:
            today = datetime.now()
            self.slug = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + slugify(self.blog_title)
        super().save(*args, **kwargs)
        if self.image1:
            self.resize_image(self.image1)
        if self.image2:
            self.resize_image(self.image2)
        if self.image3:
            self.resize_image(self.image3)
        if self.image4:
            self.resize_image(self.image4)

    def resize_image(self, input_image):
        memfile = BytesIO()
        image = Image.open(input_image)
        image_size = image.size
        resize = (400, 300)
        if image_size != resize:
            resized_image = image.resize(resize)
            resized_image.save(memfile, 'JPEG', quality=95)
            storage.save(input_image.name, memfile)
            memfile.close()
            image.close()

    class Meta:
        ordering = ("order",)


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
