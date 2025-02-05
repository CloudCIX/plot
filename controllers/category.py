# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from plot.models import Category


__all__ = [
    'CategoryCreateController',
    'CategoryListController',
    'CategoryUpdateController',
]


class CategoryListController(ControllerBase):
    """
    Validates User data used to list Category records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'name',
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


class CategoryCreateController(ControllerBase):
    """
    Validates user data used to create Category records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Category
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Category
        type: string
        """
        if name is None:
            return 'plot_category_create_101'
        name = str(name).strip()
        if len(name) == 0:
            return 'plot_category_create_102'
        if len(name) > self.get_field('name').max_length:
            return 'plot_category_create_103'
        if Category.objects.filter(name=name, address_id=self.request.user.address['id']).exists():
            return 'plot_category_create_104'
        self.cleaned_data['name'] = name
        return None


class CategoryUpdateController(ControllerBase):
    """
    Validates User data used to update a Category
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Category
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Category
        type: string
        """
        if name is None:
            return 'plot_category_update_101'
        name = str(name).strip()
        if len(name) == 0:
            return 'plot_category_update_102'
        if len(name) > self.get_field('name').max_length:
            return 'plot_category_update_103'
        if Category.objects.filter(
                name=name,
                address_id=self.request.user.address['id'],
        ).exclude(pk=self._instance.pk).exists():
            return 'plot_category_update_104'
        self.cleaned_data['name'] = name
        return None
