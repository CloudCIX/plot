# libs
from cloudcix_rest.controllers import ControllerBase
# local

__all__ = [
    'SourceSummaryListController',
]


class SourceSummaryListController(ControllerBase):
    """
    Validates Source Summary data used to filter a list of Reading records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the Controller.Meta fields
        """
        allowed_ordering = (
            'datetime_taken',
        )
        search_fields = {
            'end_date': (),
            'interval': (),
            'start_date': (),
        }
