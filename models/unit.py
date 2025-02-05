# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse


__all__ = [
    'Unit',
]


class Unit(BaseModel):
    """
    A Unit record represents the Unit a Source will be measured in
    """
    abbreviation = models.CharField(max_length=5)
    address_id = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'unit'
        indexes = [
            models.Index(fields=['address_id'], name='unit_address_id'),
            models.Index(fields=['id'], name='unit_id'),
            models.Index(fields=['name'], name='unit_name'),
        ]
        ordering = ['name']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the Unit Resource view for this Unit record
        :return: A URL that corresponds to the views for this Unit record
        """
        return reverse('unit_resource', kwargs={'pk': self.pk})
