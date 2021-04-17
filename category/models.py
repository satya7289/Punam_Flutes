from django.db import models
from commons.models import TimeStampedModel


class Category(TimeStampedModel):

    display_name = models.CharField(max_length=200, null=False)
    description = models.TextField()
    order = models.PositiveIntegerField(blank=True, null=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name

    class Meta:
        ordering = ("order","display_name")
