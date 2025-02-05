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
from plot.models import Source, Unit


class Permissions:

    @staticmethod
    def read(request: Request, obj: Unit) -> Optional[Http403]:
        """
        The request to read a Unit object is valid if:
        - The User's Address owns the Unit.
        - The User is global active and an address in their Member owns the Unit
        """
        # The User's Address owns the Unit of the Source.
        if request.user.address['id'] != obj.address_id:
            if not request.user.global_active:
                return Http403(error_code='plot_unit_read_201')
            # The User is global active and an address in their Member owns the Unit of the Source.
            response = Membership.address.read(
                token=request.user.token,
                pk=obj.address_id)
            if response.status_code != 200 or response.json()['content']['member']['id'] != request.user.member['id']:
                return Http403(error_code='plot_unit_read_202')
        return None

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new unit record is valid if:
        - The User creating a unit record is a self-managed Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='plot_unit_create_201')
        return None

    @staticmethod
    def delete(request: Request, obj: Unit) -> Optional[Http403]:
        """
        The request to delete a Unit record is valid if:
        - There are no Sources associated with the Unit
        """
        # There are no Sources associated with the Unit
        if Source.objects.filter(unit=obj, deleted__isnull=True).exists():
            return Http403(error_code='plot_unit_delete_201')
        return None
