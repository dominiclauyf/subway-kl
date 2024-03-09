from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models


# Create your models here.
class SubwayOutlet(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    operating_time = models.CharField(max_length=100)
    long = models.DecimalField(decimal_places=4, max_digits=10)
    lat = models.DecimalField(decimal_places=4, max_digits=10)
    retrieve_long = models.DecimalField(
        decimal_places=4, max_digits=10, null=True, blank=True
    )
    retrieve_lat = models.DecimalField(
        decimal_places=4, max_digits=10, null=True, blank=True
    )

    def __str__(self):
        return self.name
