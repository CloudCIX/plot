# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .source import Source

__all__ = [
    'Reading',
]


class ReadingManager(BaseManager):
    """
    Manager for Readings which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'source',
        )


class Reading(BaseModel):
    """
    A Reading record represents a reading for a source
    """
    datetime_taken = models.DateTimeField()
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='readings')
    value = models.DecimalField(decimal_places=2, max_digits=10)

    objects = ReadingManager()

    class Meta:
        db_table = 'reading'
        indexes = [
            models.Index(fields=['datetime_taken'], name='reading_datetime_taken'),
            models.Index(fields=['id'], name='reading_id'),
            models.Index(fields=['value'], name='reading_value'),
        ]
        ordering = ['-datetime_taken']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the Reading Resource view for this Reading record
        :return: A URL that corresponds to the views for this Reading record
        """
        return reverse('reading_resource', kwargs={'pk': self.pk})
