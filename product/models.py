from django.db import models
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
    description = models.TextField()
    category = models.ManyToManyField(Category, blank=True)
    images = models.ManyToManyField(ProductImage, blank=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("publish", "title", "search_tags")


class CountryCurrency(TimeStampedModel):
    country = models.CharField(
        max_length=100, blank=True, choices=Country, null=True, default='')
    currency = models.CharField(
        max_length=30, blank=True, null=True)
    MRP = models.DecimalField(
        decimal_places=2, max_digits=20, default=0.0)
    selling_price = models.DecimalField(
        decimal_places=2, max_digits=20, default=0.0)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)

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
