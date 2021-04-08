from django.db import models
from category.models import Category

import json
# Create your models here.

country = [['India', 'India'], ['Other', 'Other']]
METHOD_CHOICES = (
        ('percent', 'Percent'),
        ('fixed_amount', 'Fixed Amout'),
    )

GST_TYPE = [['IGST', 'IGST'], ['CGST', 'CGST'], ['SGST','SGST']]

class GSTState(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    code = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class TaxRule(models.Model):
    display_name = models.CharField(max_length=200)
    gst_type = models.CharField(max_length=10, choices=GST_TYPE, null=True, blank=True)
    description = models.TextField()
    category = models.ManyToManyField(Category, blank=True)
    country = models.CharField(max_length=100, choices=country, null=True, default='')
    state = models.ManyToManyField(GSTState, blank=True)
    method = models.CharField(choices=METHOD_CHOICES, default='percent', max_length=20)
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)

    def __str__(self):
        return self.display_name
