# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
from datetime import datetime
from decimal import Decimal, InvalidOperation
# local
from plot.models import Reading, Source


__all__ = [
    'ReadingListController',
    'ReadingCreateController',
    'ReadingUpdateController',
]


class ReadingListController(ControllerBase):
    """
    Validates User data used to list Reading records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            '-datetime_taken',
            'id',
            'source__description',
        )
        search_fields = {
            'datetime_taken': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'source_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'source__address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'source__description': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'value': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class ReadingCreateController(ControllerBase):
    """
    Validates user data used to create Reading records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Reading
        validation_order = (
            'source_id',
            'datetime_taken',
            'value',
        )

    def validate_source_id(self, source_id: Optional[int]) -> Optional[str]:
        """
        description: source id should belong to requesting user's source
        type: integer
        """
        if source_id is None:
            return 'plot_reading_create_101'
        try:
            source_id = int(source_id)
            source = Source.objects.get(
                id=source_id,
                category__address_id=self.request.user.address['id'],
            )
        except (ValueError, TypeError):
            return 'plot_reading_create_102'
        except Source.DoesNotExist:
            return 'plot_reading_create_103'

        self.cleaned_data['source'] = source
        return None

    def validate_datetime_taken(self, date_reading: Optional[str]) -> Optional[str]:
        """
        description: The date and time of the Reading
        type: string
        """
        try:
            datetime_taken = datetime.strptime(str(date_reading), '%Y-%m-%dT%H:%M:%S')
        except (TypeError, ValueError):
            return 'plot_reading_create_104'
        if datetime_taken > datetime.utcnow():
            return 'plot_reading_create_105'
        if 'source' not in self.cleaned_data:
            return None
        source = self.cleaned_data['source']
        if Reading.objects.filter(source=source, datetime_taken=datetime_taken).exists():
            return 'plot_reading_create_106'

        self.cleaned_data['datetime_taken'] = datetime_taken
        return None

    def validate_value(self, value: Optional[Decimal]) -> Optional[str]:
        """
        description: The value of the Reading
        type: string
        format: decimal
        """
        if value is None:
            return 'plot_reading_create_107'
        try:
            value = Decimal(str(value))
        except (ValueError, TypeError, InvalidOperation):
            return 'plot_reading_create_108'
        self.cleaned_data['value'] = value
        return None


class ReadingUpdateController(ControllerBase):
    """
    Validates user data used to create Reading records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Reading
        validation_order = (
            'datetime_taken',
            'value',
        )

    def validate_datetime_taken(self, date_reading: Optional[str]) -> Optional[str]:
        """
        description: The date and time of the Reading
        type: string
        """
        try:
            datetime_taken = datetime.strptime(str(date_reading), '%Y-%m-%dT%H:%M:%S')
        except (TypeError, ValueError):
            return 'plot_reading_update_101'
        if datetime_taken > datetime.utcnow():
            return 'plot_reading_update_102'
        if Reading.objects.filter(
            source=self._instance.source,
            datetime_taken=datetime_taken,
        ).exclude(pk=self._instance.pk).exists():
            return 'plot_reading_update_103'
        self.cleaned_data['datetime_taken'] = datetime_taken
        return None

    def validate_value(self, value: Optional[Decimal]) -> Optional[str]:
        """
        description: The value of the Reading
        type: string
        format: decimal
        """
        if value is None:
            return 'plot_reading_update_104'
        try:
            value = Decimal(str(value))
        except (ValueError, TypeError, InvalidOperation):
            return 'plot_reading_update_105'
        self.cleaned_data['value'] = value
        return None
