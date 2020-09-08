from django.db import models


class Category(models.Model):

    display_name = models.CharField(max_length=200, null=False)
    description = models.TextField()

    def __str__(self):
        return self.display_name
