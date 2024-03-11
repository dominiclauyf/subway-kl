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

    def to_context(self):
        return f"{self.name} located at {self.address}. {self.name} operation on {self.operating_time}."


class SubwayContext(models.Model):
    context = models.TextField()

    def save(self, *args, **kwargs):
        # Check if there's already an existing instance
        existing_instance = SubwayContext.objects.first()

        if existing_instance:
            # If an instance already exists, update its fields
            existing_instance.context = self.context

        super(SubwayContext, self).save(*args, **kwargs)
