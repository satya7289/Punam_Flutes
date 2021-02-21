from django.db import models

class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        abstract = True