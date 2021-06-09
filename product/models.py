from django.db import models
from django.utils.text import slugify
from storages.backends.s3boto3 import S3Boto3Storage
from commons.country_currency import country as Country
from django.conf import settings

from category.models import Category
from commons.models import TimeStampedModel

InventoryType = [['limited', 'limited'], ['unlimited', 'unlimited']]


class ProductImage(TimeStampedModel):
    """
    Models to store all the uploaded product images to S3 bucket.
    """
    image = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=False, null=False, upload_to='productImage/%Y%m%d%M%S')
    # image = models.ImageField(upload_to='productImage/')

    def __str__(self):
        return str(self.image)


class Product(TimeStampedModel):
    title = models.CharField(max_length=200, default='Flute')
    search_tags = models.CharField(max_length=200)
    sku = models.CharField(max_length=256, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    customization_description = models.TextField(blank=True, null=True)
    generic_name = models.CharField(max_length=512, blank=True, null=True)
    manufacture = models.CharField(max_length=512, blank=True, null=True)
    region_of_origin = models.CharField(max_length=512, blank=True, null=True)
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

# class Product(models.Model):
#     title = models.CharField(max_length=200, default='Flute')
#     search_tags = models.CharField(max_length=200)
#     description = models.TextField()
#     category = models.OneToOneField(
#         'category.Category', on_delete=models.CASCADE)
#     image = models.OneToOneField(
#         'product.ProductImage', on_delete=models.CASCADE, default=None)

#     def __str__(self):
#         return self.title

# class Product(models.Model):
#     title = models.CharField(max_length=200, default='Flute')
#     search_tags = models.CharField(max_length=200)
#     description = models.TextField()
#     category = models.OneToOneField(
#         'category.Category', on_delete=models.CASCADE)
#     image = models.OneToOneField(
#         'product.ProductImage', on_delete=models.CASCADE, default=None)

#     def __str__(self):
#         return self.title


# class ProductImage(models.Model):
#     """
#     Models to store all the uploaded product images to S3 bucket.

#     """

#     product_image_1 = models.ImageField(storage=S3Boto3Storage(
#         bucket='punam-flutes-prods'), blank=False, null=False)
#     product_image_2 = models.ImageField(storage=S3Boto3Storage(
#         bucket='punam-flutes-prods'), blank=True, null=True)
#     product_image_3 = models.ImageField(storage=S3Boto3Storage(
#         bucket='punam-flutes-prods'), blank=True, null=True)
#     product_image_4 = models.ImageField(storage=S3Boto3Storage(
#         bucket='punam-flutes-prods'), blank=True, null=True)
#     product_image_5 = models.ImageField(storage=S3Boto3Storage(
#         bucket='punam-flutes-prods'), blank=True, null=True)
#     product_image_6 = models.ImageField(storage=S3Boto3Storage(
#         bucket='punam-flutes-prods'), blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.product_image_1)
