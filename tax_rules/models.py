from django.db import models
from django_countries.fields import CountryField

# Create your models here.


class TaxRule(models.Model):
    display_name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    country = CountryField()
    state = models.CharField(max_length=1024)
    METHOD_CHOICES = (
        ('percent', 'Percent'),
        ('fixed_amount', 'Fixed Amout'),
    )
    method = models.CharField(
        choices=METHOD_CHOICES,
        default='percent',
        max_length=20
    )

    value = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)

    def __str__(self):
        return self.display_name
