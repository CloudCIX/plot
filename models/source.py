# libs
from cloudcix_rest.models import BaseManager, BaseModel
from datetime import datetime
from django.db import models
from django.urls import reverse
# local
from .category import Category
from .unit import Unit


__all__ = [
    'Source',
]


class SourceManager(BaseManager):
    """
    Manager for Sources which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'category',
            'unit',
        )


class Source(BaseModel):
    """
    A Source record represents a Source of readings for monitoring purposes
    """
    accumulating = models.BooleanField(default=False)
    amber_high = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    amber_low = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='sources')
    description = models.CharField(max_length=50)
    red_high = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    red_low = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    retention = models.IntegerField(default=3650)
    seconds_valid = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='sources')

    objects = SourceManager()

    class Meta:
        db_table = 'source'
        indexes = [
            models.Index(fields=['accumulating'], name='source_accumulating'),
            models.Index(fields=['amber_high'], name='source_amber_high'),
            models.Index(fields=['amber_low'], name='source_amber_low'),
            models.Index(fields=['description'], name='source_description'),
            models.Index(fields=['id'], name='source_id'),
            models.Index(fields=['red_high'], name='source_red_high'),
            models.Index(fields=['red_low'], name='source_red_low'),
            models.Index(fields=['retention'], name='source_retention'),
            models.Index(fields=['seconds_valid'], name='source_seconds_valid'),
        ]
        ordering = ['description']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the Source Resource view for this Source record
        :return: A URL that corresponds to the views for this Source record
        """
        return reverse('source_resource', kwargs={'pk': self.pk})

    def cascade_delete(self):
        """
        Delete the Source instance, and the shares and readings associated with it
        """
        deltime = datetime.utcnow()
        self.readings.all().update(deleted=deltime)
        self.shares.all().update(deleted=deltime)
        self.deleted = deltime
        self.save()
