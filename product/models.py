from django.db import models
from django_countries.fields import CountryField
from storages.backends.s3boto3 import S3Boto3Storage
from commons.country_currency import country, currency
from django.conf import settings

from category.models import Category
from commons.models import TimeStampedModel

InventoryType = [['limited', 'limited'], ['unlimited', 'unlimited']]

class ProductImage(TimeStampedModel):
    """
    Models to store all the uploaded product images to S3 bucket.
    """
    image = models.ImageField(storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME), blank=False, null=False,upload_to='productImage/%Y%m%d%M%S')
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
        max_length=100, blank=True, choices=country, null=True, default='')
    currency = models.CharField(
        max_length=30, blank=True, choices=currency, null=True, default='')
    MRP = models.DecimalField(
        decimal_places=2, max_digits=20, default=0.0)
    selling_price = models.DecimalField(
        decimal_places=2, max_digits=20, default=0.0)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Country Currencies"
    
    def __str__(self):
        return self.currency + ' ' + self.country

class Inventory(TimeStampedModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=InventoryType, blank=True, null=True)
    available = models.PositiveIntegerField(blank=True, null=True)
    sold = models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.product.title


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
