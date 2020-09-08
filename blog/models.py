from django.db import models

# Create your models here.


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
