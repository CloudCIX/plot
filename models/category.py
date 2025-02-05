# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse


__all__ = [
    'Category',
]


class Category(BaseModel):
    """
    A Category record represents a grouping object for Sources
    """
    address_id = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'category'
        indexes = [
            models.Index(fields=['address_id'], name='category_address_id'),
            models.Index(fields=['id'], name='category_id'),
            models.Index(fields=['name'], name='category_name'),
        ]
        ordering = ['name']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the Category Resource view for this Category record
        :return: A URL that corresponds to the views for this Category record
        """
        return reverse('category_resource', kwargs={'pk': self.pk})
