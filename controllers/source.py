# stdlib
from decimal import Decimal, InvalidOperation
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from plot.models import Category, Source, Unit


__all__ = [
    'SourceListController',
    'SourceCreateController',
    'SourceUpdateController',
]


class SourceListController(ControllerBase):
    """
    Validates User data used to list Source records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'description',
            'created',
            'id',
            'updated',
        )
        search_fields = {
            'accumulating': (),
            'amber_high': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'amber_low': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'category_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'category__address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'category__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'description': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'red_high': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'red_low': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'retention': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'seconds_valid': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'unit_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'unit__address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'unit__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class SourceCreateController(ControllerBase):
    """
    Validates user data used to create Source records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Source
        validation_order = (
            'accumulating',
            'category_id',
            'description',
            'seconds_valid',
            'unit_id',
            'red_high',
            'amber_high',
            'amber_low',
            'red_low',
            'retention',
        )

    def validate_accumulating(self, accumulating: Optional[bool]) -> Optional[str]:
        """
        description: Flag to state if the readings of the Source is accumulating.
        type: boolean
        required: false
        """
        if accumulating is None:
            accumulating = False
        if not isinstance(accumulating, bool):
            return 'plot_source_create_101'

        self.cleaned_data['accumulating'] = accumulating
        return None

    def validate_category_id(self, category_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Category for the Source
        type: integer
        """
        if category_id is None:
            return 'plot_source_create_102'

        try:
            category_id = int(category_id)
            category = Category.objects.get(id=category_id, address_id=self.request.user.address['id'])
        except (ValueError, TypeError):
            return 'plot_source_create_103'
        except Category.DoesNotExist:
            return 'plot_source_create_104'

        self.cleaned_data['category'] = category
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: The description of the Source
        type: string
        """
        if description is None:
            description = ''
        description = str(description).strip()
        if len(description) == 0:
            return 'plot_source_create_105'

        if len(description) > self.get_field('description').max_length:
            return 'plot_source_create_106'

        if 'category' not in self.cleaned_data:
            return None

        if Source.objects.filter(description=description, category=self.cleaned_data['category']).exists():
            return 'plot_source_create_107'

        self.cleaned_data['description'] = description
        return None

    def validate_seconds_valid(self, seconds_valid: Optional[int]) -> Optional[str]:
        """
        description: The number of seconds that the Readings for the Source is valid for
        type: integer
        """
        if seconds_valid is None:
            return 'plot_source_create_108'

        try:
            seconds_valid = int(seconds_valid)
        except (TypeError, ValueError):
            return 'plot_source_create_109'

        if seconds_valid <= 0:
            return 'plot_source_create_110'

        self.cleaned_data['seconds_valid'] = seconds_valid
        return None

    def validate_unit_id(self, unit_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Unit the Source will be measured in
        type: integer
        """
        if unit_id is None:
            return 'plot_source_create_111'

        try:
            unit_id = int(unit_id)
            unit = Unit.objects.get(id=unit_id, address_id=self.request.user.address['id'])
        except (ValueError, TypeError):
            return 'plot_source_create_112'
        except Unit.DoesNotExist:
            return 'plot_source_create_113'

        self.cleaned_data['unit'] = unit
        return None

    def validate_red_high(self, red_high: Optional[str]) -> Optional[str]:
        """
        description: The high threshold of the readings that should trigger a red alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' not in self.cleaned_data or self.cleaned_data['accumulating'] is True:
            return None

        try:
            red_high_decimal = Decimal(str(red_high))
        except InvalidOperation:
            return 'plot_source_create_114'

        self.cleaned_data['red_high'] = red_high_decimal
        return None

    def validate_amber_high(self, amber_high: Optional[str]) -> Optional[str]:
        """
        description: The high threshold of the readings that should trigger an amber alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' not in self.cleaned_data or self.cleaned_data['accumulating'] is True:
            return None

        try:
            amber_high_decimal = Decimal(str(amber_high))
        except InvalidOperation:
            return 'plot_source_create_115'

        if 'red_high' not in self.cleaned_data:
            return None

        if amber_high_decimal >= self.cleaned_data['red_high']:
            return 'plot_source_create_116'

        self.cleaned_data['amber_high'] = amber_high_decimal
        return None

    def validate_amber_low(self, amber_low: Optional[str]) -> Optional[str]:
        """
        description: The low threshold of the readings that should trigger an amber alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' not in self.cleaned_data or self.cleaned_data['accumulating'] is True:
            return None

        try:
            amber_low_decimal = Decimal(str(amber_low))
        except InvalidOperation:
            return 'plot_source_create_117'

        if 'amber_high' not in self.cleaned_data:
            return None

        if amber_low_decimal >= self.cleaned_data['amber_high']:
            return 'plot_source_create_118'

        self.cleaned_data['amber_low'] = amber_low_decimal
        return None

    def validate_red_low(self, red_low: Optional[str]) -> Optional[str]:
        """
        description: The low threshold of the readings that should trigger a red alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' not in self.cleaned_data or self.cleaned_data['accumulating'] is True:
            return None

        try:
            red_low_decimal = Decimal(str(red_low))
        except InvalidOperation:
            return 'plot_source_create_119'

        if 'amber_low' not in self.cleaned_data:
            return None

        if red_low_decimal >= self.cleaned_data['amber_low']:
            return 'plot_source_create_120'

        self.cleaned_data['red_low'] = red_low_decimal
        return None

    def validate_retention(self, retention: Optional[int]) -> Optional[str]:
        """
        description: |
            The number of days that the Readings for the Source will be retained. Default is for 3650 days (10 years)
        type: integer
        required: false
        """
        if retention is None:
            retention = 3650

        try:
            retention = int(retention)
        except (TypeError, ValueError):
            return 'plot_source_create_121'

        if retention <= 0:
            return 'plot_source_create_122'

        self.cleaned_data['retention'] = retention
        return None


class SourceUpdateController(ControllerBase):
    """
    Validates user data used to create Source records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Source
        validation_order = (
            'accumulating',
            'category_id',
            'description',
            'seconds_valid',
            'unit_id',
            'red_high',
            'amber_high',
            'amber_low',
            'red_low',
            'retention',
        )

    def validate_accumulating(self, accumulating: Optional[bool]) -> Optional[str]:
        """
        description: Flag to state if the readings of the Source is accumulating.
        type: boolean
        required: false
        """
        if accumulating is None:
            return None
        if not isinstance(accumulating, bool):
            return 'plot_source_update_101'

        self.cleaned_data['accumulating'] = accumulating
        return None

    def validate_category_id(self, category_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Category for the Source
        type: integer
        """
        if category_id is None:
            return 'plot_source_update_102'

        if category_id == self._instance.category.pk:
            return None

        try:
            category_id = int(category_id)
            category = Category.objects.get(id=category_id, address_id=self.request.user.address['id'])
        except (ValueError, TypeError):
            return 'plot_source_update_103'
        except Category.DoesNotExist:
            return 'plot_source_update_104'

        self.cleaned_data['category'] = category
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: The description of the Source
        type: string
        """
        if description is None:
            description = ''
        description = str(description).strip()
        if len(description) == 0:
            return 'plot_source_update_105'

        if len(description) > self.get_field('description').max_length:
            return 'plot_source_update_106'

        if 'category_id' in self._errors:
            return None

        category = self.cleaned_data.get('category', self._instance.category)
        if Source.objects.filter(description=description, category=category).exclude(pk=self._instance.pk).exists():
            return 'plot_source_update_107'

        self.cleaned_data['description'] = description
        return None

    def validate_seconds_valid(self, seconds_valid: Optional[int]) -> Optional[str]:
        """
        description: The number of seconds that the Readings for the Source is valid for
        type: integer
        """
        if seconds_valid is None:
            return 'plot_source_update_108'

        try:
            seconds_valid = int(seconds_valid)
        except (TypeError, ValueError):
            return 'plot_source_update_109'

        if seconds_valid <= 0:
            return 'plot_source_update_110'

        self.cleaned_data['seconds_valid'] = seconds_valid
        return None

    def validate_unit_id(self, unit_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Unit the Source will be measured in
        type: integer
        """
        if unit_id is None:
            return 'plot_source_update_111'

        if unit_id == self._instance.unit.pk:
            return None

        try:
            unit_id = int(unit_id)
            unit = Unit.objects.get(id=unit_id, address_id=self.request.user.address['id'])
        except (ValueError, TypeError):
            return 'plot_source_update_112'
        except Unit.DoesNotExist:
            return 'plot_source_update_113'

        self.cleaned_data['unit'] = unit
        return None

    def validate_red_high(self, red_high: Optional[str]) -> Optional[str]:
        """
        description: The high threshold of the readings that should trigger a red alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' in self._errors:
            return None
        accumulating = self.cleaned_data.get('accumulating', self._instance.accumulating)
        if accumulating is True:
            return None

        try:
            red_high_decimal = Decimal(str(red_high))
        except InvalidOperation:
            return 'plot_source_update_114'

        self.cleaned_data['red_high'] = red_high_decimal
        return None

    def validate_amber_high(self, amber_high: Optional[str]) -> Optional[str]:
        """
        description: The high threshold of the readings that should trigger an amber alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' in self._errors:
            return None
        accumulating = self.cleaned_data.get('accumulating', self._instance.accumulating)
        if accumulating is True:
            return None

        try:
            amber_high_decimal = Decimal(str(amber_high))
        except InvalidOperation:
            return 'plot_source_update_115'

        if 'red_high' in self._errors:
            return None

        red_high = self.cleaned_data.get('red_high', self._instance.red_high)
        if amber_high_decimal >= red_high:
            return 'plot_source_update_116'

        self.cleaned_data['amber_high'] = amber_high_decimal
        return None

    def validate_amber_low(self, amber_low: Optional[str]) -> Optional[str]:
        """
        description: The low threshold of the readings that should trigger an amber alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' in self._errors:
            return None
        accumulating = self.cleaned_data.get('accumulating', self._instance.accumulating)
        if accumulating is True:
            return None

        try:
            amber_low_decimal = Decimal(str(amber_low))
        except InvalidOperation:
            return 'plot_source_update_117'

        if 'amber_high' in self._errors:
            return None

        amber_high = self.cleaned_data.get('amber_high', self._instance.amber_high)
        if amber_low_decimal >= amber_high:
            return 'plot_source_update_118'

        self.cleaned_data['amber_low'] = amber_low_decimal
        return None

    def validate_red_low(self, red_low: Optional[str]) -> Optional[str]:
        """
        description: The low threshold of the readings that should trigger a red alert
        type: string
        format: decimal
        required: false
        """
        if 'accumulating' in self._errors:
            return None
        accumulating = self.cleaned_data.get('accumulating', self._instance.accumulating)
        if accumulating is True:
            return None

        try:
            red_low_decimal = Decimal(str(red_low))
        except InvalidOperation:
            return 'plot_source_update_119'

        if 'amber_low' in self._errors:
            return None

        amber_low = self.cleaned_data.get('amber_low', self._instance.amber_low)
        if red_low_decimal >= amber_low:
            return 'plot_source_update_120'

        self.cleaned_data['red_low'] = red_low_decimal
        return None

    def validate_retention(self, retention: Optional[int]) -> Optional[str]:
        """
        description: |
            The number of days that the Readings for the Source will be retained. Default is for 3650 days (10 years)
        type: integer
        required: false
        """
        if retention is None:
            return None

        try:
            retention = int(retention)
        except (TypeError, ValueError):
            return 'plot_source_update_121'

        if retention <= 0:
            return 'plot_source_update_122'

        self.cleaned_data['retention'] = retention
        return None
