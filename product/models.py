from django.db import models
from django.utils.text import slugify
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

from category.models import Category
from commons.models import TimeStampedModel

from PIL import Image
from io import BytesIO

InventoryType = [['limited', 'limited'], ['unlimited', 'unlimited']]
Continent = (
    ('Asia', 'Asia'),
    ('Africa', 'Africa'),
    ('Europe', 'Europe'),
    ('NAmerica', 'North America'),
    ('SAmerica', 'South America'),
    ('Australia', 'Australia'),
)

PRODUCT_IMAGE_DIR = 'productImage'
storage = S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME)

# Resize image sizes


class ProductImage(TimeStampedModel):
    """
    Models to store all the uploaded product images to S3 bucket.
    """
    image = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=False, null=False, upload_to=PRODUCT_IMAGE_DIR + '/%Y%m%d%M%S')
    image_list = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=True, null=True, upload_to=PRODUCT_IMAGE_DIR + '/%Y%m%d%M%S')
    image_detail = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=True, null=True, upload_to=PRODUCT_IMAGE_DIR + '/%Y%m%d%M%S')
    image_small = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=True, null=True, upload_to=PRODUCT_IMAGE_DIR + '/%Y%m%d%M%S')
    image_big = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=True, null=True, upload_to=PRODUCT_IMAGE_DIR + '/%Y%m%d%M%S')
    # image = models.ImageField(upload_to='productImage/')

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    def get_resize(self, original_size, resize_with):
        w, h = original_size
        ratio = w / h
        if ratio > 1:
            return (resize_with, int(resize_with // ratio))
        else:
            return (int(resize_with * ratio), resize_with)

    def get_resized_image(self, image, resize_size):
        memfile = BytesIO()
        resized_image = image.resize(resize_size)
        rgb_resized_image = resized_image.convert('RGB')
        rgb_resized_image.save(memfile, 'JPEG', quality=95)
        return memfile

    def resize_image(self):
        input_image = self.image
        input_list_image = self.image_list
        input_detail_image = self.image_detail
        # input_small_image = self.image_small
        # input_big_image = self.image_big
        image_name = input_image.name

        image = Image.open(input_image)  # fetch the image
        image_size = image.size  # Get the size of the image

        # for the list image resize_with(320)
        list_resize = self.get_resize(image_size, 320)
        filename = f'resized_{list_resize[0]}_{list_resize[1]}_{image_name}'
        if input_list_image:
            list_image = Image.open(input_list_image)
            list_image_size = list_image.size
            if list_resize != list_image_size:
                memfile = self.get_resized_image(image, list_resize)
                self.image_list.save(filename, memfile)
                memfile.close()
        else:
            memfile = self.get_resized_image(image, list_resize)
            self.image_list.save(filename, memfile)
            memfile.close()

        # for the detail image (450, 450) if same otherwaise resize_with(355)
        if image_size[0] == image_size[1]:
            detail_resize = (450, 450)
        else:
            detail_resize = self.get_resize(image_size, 355)
        filename = f'resized_{detail_resize[0]}_{detail_resize[1]}_{image_name}'
        if input_detail_image:
            detail_image = Image.open(input_detail_image)
            detail_image_size = detail_image.size
            if detail_resize != detail_image_size:
                memfile = self.get_resized_image(image, detail_resize)
                self.image_detail.save(filename, memfile)
                memfile.close()
        else:
            memfile = self.get_resized_image(image, detail_resize)
            self.image_detail.save(filename, memfile)
            memfile.close()

        # # for the small image: (40, 40)
        # small_resize = (40, 40)
        # filename = f'resized_{small_resize[0]}_{small_resize[1]}_{image_name}'
        # if input_small_image:
        #     small_image = Image.open(input_small_image)
        #     small_image_size = small_image.size
        #     if small_resize != small_image_size:
        #         memfile = self.get_resized_image(image, small_resize)
        #         self.image_small.save(filename, memfile)
        #         memfile.close()
        # else:
        #     memfile = self.get_resized_image(image, small_resize)
        #     self.image_small.save(filename, memfile)
        #     memfile.close()

        # # for the big image: size: (1500, 1500)
        # big_reize = (1500, 1500)
        # filename = f'resized_{big_reize[0]}_{big_reize[1]}_{image_name}'
        # if input_big_image:
        #     big_image = Image.open(input_big_image)
        #     big_image_size = big_image.size
        #     if big_reize != big_image_size:
        #         memfile = self.get_resized_image(image, big_reize)
        #         self.image_big.save(filename, memfile)
        #         memfile.close()
        # else:
        #     memfile = self.get_resized_image(image, big_reize)
        #     self.image_big.save(filename, memfile)
        #     memfile.close()


class Product(TimeStampedModel):
    title = models.CharField(max_length=200, default='Flute')
    search_tags = models.CharField(max_length=200)
    sku = models.CharField(max_length=256, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    customization_description = models.TextField(blank=True, null=True)
    generic_name = models.CharField(max_length=512, blank=True, null=True)
    manufacture = models.CharField(max_length=512, blank=True, null=True)
    country_of_origin = models.CharField(max_length=512, blank=True, null=True)
    material = models.CharField(max_length=512, blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)
    images = models.ManyToManyField(ProductImage, blank=True)
    slug = models.SlugField(max_length=1024, blank=True, null=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("publish", "title", "search_tags")


class CountryCurrency(TimeStampedModel):
    country = models.CharField(max_length=255, blank=True, null=True, default='')
    currency = models.CharField(max_length=30, blank=True, null=True)
    MRP = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    selling_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    shipping_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.0, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Country Currencies"

    def __str__(self):
        return self.country


class Inventory(TimeStampedModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=InventoryType, blank=True, null=True)
    available = models.PositiveIntegerField(blank=True, null=True, default=0)
    sold = models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.product.title if self.product else None


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
