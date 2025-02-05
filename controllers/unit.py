# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from plot.models import Unit


__all__ = [
    'UnitListController',
    'UnitCreateController',
    'UnitUpdateController',
]


class UnitListController(ControllerBase):
    """
    Validates User data used to list Unit records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'name',
            'abbreviation',
            'created',
            'id',
            'updated',
        )
        search_fields = {
            'address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class UnitCreateController(ControllerBase):
    """
    Validates user data used to create Unit records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Unit
        validation_order = (
            'abbreviation',
            'name',
        )

    def validate_abbreviation(self, abbreviation: Optional[str]) -> Optional[str]:
        """
        description: The abbreviation of the name for the unit - e.g cm
        type: string
        """
        if abbreviation is None:
            return 'plot_unit_create_101'
        abbreviation = str(abbreviation).strip()
        if len(abbreviation) == 0:
            return 'plot_unit_create_102'
        if len(abbreviation) > self.get_field('abbreviation').max_length:
            return 'plot_unit_create_103'
        self.cleaned_data['abbreviation'] = abbreviation
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description:  The name given to the Unit e.g. centimetres
        type: string
        """
        if name is None:
            return 'plot_unit_create_104'
        name = str(name).strip()
        if len(name) == 0:
            return 'plot_unit_create_105'
        if len(name) > self.get_field('name').max_length:
            return 'plot_unit_create_106'
        if 'abbreviation' not in self.cleaned_data:
            return None
        if Unit.objects.filter(
            abbreviation=self.cleaned_data['abbreviation'],
            address_id=self.request.user.address['id'],
            name=name,
        ).exists():
            return 'plot_unit_create_107'
        self.cleaned_data['name'] = name
        return None


class UnitUpdateController(ControllerBase):
    """
    Validates User data used to update a Unit
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Unit
        validation_order = (
            'abbreviation',
            'name',
        )

    def validate_abbreviation(self, abbreviation: Optional[str]) -> Optional[str]:
        """
        description: The abbreviation of the name for the unit - e.g cm
        type: string
        """
        if abbreviation is None:
            return 'plot_unit_update_101'
        abbreviation = str(abbreviation).strip()
        if len(abbreviation) == 0:
            return 'plot_unit_update_102'
        if len(abbreviation) > self.get_field('abbreviation').max_length:
            return 'plot_unit_update_103'
        self.cleaned_data['abbreviation'] = abbreviation
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name given to the Unit e.g. centimetres
        type: string
        """
        if name is None:
            return 'plot_unit_update_104'
        name = str(name).strip()
        if len(name) == 0:
            return 'plot_unit_update_105'
        if len(name) > self.get_field('name').max_length:
            return 'plot_unit_update_106'
        if 'abbreviation' in self._errors:
            return None
        abbreviation = self.cleaned_data.get('abbreviation', self._instance.abbreviation)
        if Unit.objects.filter(
            abbreviation=abbreviation,
            address_id=self.request.user.address['id'],
            name=name,
        ).exclude(pk=self._instance.pk).exists():
            return 'plot_unit_update_107'
        self.cleaned_data['name'] = name
        return None
