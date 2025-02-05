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
from rest_framework.request import Request
# local
from plot.models import Source, SourceShare
from plot.utils import get_addresses_in_member


class Permissions:

    @staticmethod
    def list(request: Request, obj: Source) -> Optional[Http403]:
        """
        The request to run a Source Summary for a Source is Valid if:
        - The User's Address owns the Category of the Source.
        - The Source has been Shared with the User's Address
        - The User is global active and an address in their Member owns the Category of the Source.
        - The User is global active and the Source has been shared with an address in their Member.
        """
        # The User's Address owns the Category of the Source
        if request.user.address['id'] != obj.category.address_id:
            # Source has been Shared with the User's Address
            if SourceShare.objects.filter(source=obj, address_id=request.user.address['id']).exists():
                return None
            # User is global
            if not request.user.global_active:
                return Http403(error_code='plot_source_summary_list_201')
            user_member_addresses = get_addresses_in_member()
            # An address in the global users Member owns the Category of the Source
            if obj.category.address_id not in user_member_addresses:
                # Source has been shared with an address in the global users Member
                if SourceShare.objects.filter(source=obj, address_id__in=user_member_addresses).exists():
                    return None
                return Http403(error_code='plot_source_summary_list_202')

        return None
