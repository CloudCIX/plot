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


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new Reading record is valid if:
        - The User creating a Reading is a self-managed Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='plot_reading_create_201')
        return None

    @staticmethod
    def update(request: Request) -> Optional[Http403]:
        """
        The request to update a new Reading record is valid if:
        - The User updating a Reading is an Administrator
        """
        # The requesting User's Member is self-managed
        if not request.user.administrator:
            return Http403(error_code='plot_reading_update_201')
        return None

    @staticmethod
    def delete(request: Request) -> Optional[Http403]:
        """
        The request to delete a new Reading record is valid if:
        - The User deleting a Reading is an Administrator
        """
        # The requesting User's Member is self-managed
        if not request.user.administrator:
            return Http403(error_code='plot_reading_delete_201')
        return None
