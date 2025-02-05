# libs
from cloudcix_rest.controllers import ControllerBase
# local

__all__ = [
    'SourceGroupSummaryListController',
]


class SourceGroupSummaryListController(ControllerBase):
    """
    Validates Source Group Summary data used to filter a list of Source and Reading records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the Controller.Meta fields
        """
        allowed_ordering = (
            'datetime_taken',
        )
        search_fields = {
            'accumulating': (),
            'end_date': (),
            'interval': (),
            'start_date': (),
            'unit_id': (),
        }
