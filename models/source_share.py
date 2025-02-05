# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .source import Source


__all__ = [
    'SourceShare',
]


class SourceShareManager(BaseManager):
    """
    Manager for Source Share which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'source',
        )


class SourceShare(BaseModel):
    """
    A Source Share record represents the address the Readings of a Source will be shared with
    """
    address_id = models.IntegerField()
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='shares')

    objects = SourceShareManager()

    class Meta:
        db_table = 'source_share'
        indexes = [
            models.Index(fields=['address_id'], name='source_share_address_id'),
            models.Index(fields=['id'], name='source_share_id'),
        ]
        ordering = ['address_id']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the Source Share Resource view for this Source Share record
        :return: A URL that corresponds to the views for this Source Share record
        """
        return reverse('source_share_resource', kwargs={'pk': self.pk})
