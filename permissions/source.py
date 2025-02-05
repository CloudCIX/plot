"""
Permissions classes will use their methods to validate permissions for a
request.
These methods will raise any errors that may occur all you have to do is
call the method in the view
"""
# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from cloudcix.api.membership import Membership
from rest_framework.request import Request
# local
from plot.models import Source


class Permissions:

    @staticmethod
    def read(request: Request, obj: Source) -> Optional[Http403]:
        """
        The request to read a Source object is valid if:
        - The User's Address owns the Category of the Source.
        - The User is global active and an address in their Member owns the Category of the Source.
        """
        # The User's Address owns the Category of the Source.
        if request.user.address['id'] != obj.category.address_id:
            if not request.user.global_active:
                return Http403(error_code='plot_source_read_201')
            # The User is global active and an address in their Member owns the Category of the Source.
            response = Membership.address.read(
                token=request.user.token,
                pk=obj.category.address_id)
            if response.status_code != 200 or response.json()['content']['member']['id'] != request.user.member['id']:
                return Http403(error_code='plot_source_read_202')
        return None
