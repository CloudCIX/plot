# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
from cloudcix.api.membership import Membership
# local
from plot.models import Source, SourceShare


__all__ = [
    'SourceShareListController',
    'SourceShareCreateController',
]


class SourceShareListController(ControllerBase):
    """
    Validates User data used to list Source Share records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'source__description',
            'source__category__name',
            'address_id',
            'created',
            'id',
            'source_id',
            'updated',
        )
        search_fields = {
            'address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'source_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'source__category__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'source__description': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class SourceShareCreateController(ControllerBase):
    """
    Validates user data used to create Source Share records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = SourceShare
        validation_order = (
            'address_id',
            'source_id',
        )

    def validate_address_id(self, address_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Address to share the Source and its Readings with
        type: integer
        """
        if address_id is None:
            return 'plot_source_share_create_101'

        try:
            address_id = int(address_id)
        except (TypeError, ValueError):
            return 'plot_source_share_create_102'

        if address_id == self.request.user.address['id']:
            return 'plot_source_share_create_103'

        response = Membership.address.read(
            token=self.request.user.token,
            pk=address_id,
            span=self.span,
        )
        if response.status_code != 200:
            return 'plot_source_share_create_104'

        self.cleaned_data['address_id'] = address_id
        return None

    def validate_source_id(self, source_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the source record to be shared with the sent address
        type: integer
        """
        if source_id is None:
            return 'plot_source_share_create_105'

        # Ensure it belongs to the Category of the Source object belongs to the requesting users address
        try:
            source_id = int(source_id)
            source = Source.objects.get(
                id=source_id,
                category__address_id=self.request.user.address['id'],
            )
        except (TypeError, ValueError):
            return 'plot_source_share_create_106'
        except Source.DoesNotExist:
            return 'plot_source_share_create_107'

        # If the address_id was valid
        if 'address_id' not in self.cleaned_data:
            return None
        # Ensure a Source Share object does not already exist for the sent address_id and source
        if SourceShare.objects.filter(source=source, address_id=self.cleaned_data['address_id']).exists():
            return 'plot_source_share_create_108'

        self.cleaned_data['source'] = source
        return None
