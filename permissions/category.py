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
from cloudcix.api.membership import Membership
from plot.models import Category, Source


class Permissions:

    @staticmethod
    def read(request: Request, obj: Category) -> Optional[Http403]:
        """
        The request to read a Category object is valid if:
        - The User's Address owns the Category.
        - The User is global active and an address in their Member owns the Category.
        """
        # The User's Address owns the Category..
        if request.user.address['id'] != obj.address_id:
            if not request.user.global_active:
                return Http403(error_code='plot_category_read_201')
            # The User is global active and an address in their Member owns the Category of the Source.
            response = Membership.address.read(
                token=request.user.token,
                pk=obj.address_id)
            if response.status_code != 200 or response.json()['content']['member']['id'] != request.user.member['id']:
                return Http403(error_code='plot_category_read_202')
        return None

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new category record is valid if:
        - The User creating a category record is a self-managed Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='plot_category_create_201')
        return None

    @staticmethod
    def delete(request: Request, obj: Category) -> Optional[Http403]:
        """
        The request to delete a Category record is valid if:
        - There are no Sources associated with the Category
        """
        # There are no Sources associated with the Category
        if Source.objects.filter(category=obj, deleted__isnull=True).exists():
            return Http403(error_code='plot_category_delete_201')
        return None
