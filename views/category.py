"""
Management of Categories
"""
# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from plot.controllers import (
    CategoryCreateController,
    CategoryListController,
    CategoryUpdateController,
)
from plot.models import Category
from plot.permissions.category import Permissions
from plot.serializers import CategorySerializer
from plot.utils import get_addresses_in_member

__all__ = [
    'CategoryCollection',
    'CategoryResource',
]


class CategoryCollection(APIView):
    """
    Handles methods regarding Category records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Category records

        description: |
            Retrieve a list of the Category records for the requesting User's Member.

        responses:
            200:
                description: A list of the category records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        # validating controller
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CategoryListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        # setting address filter
        with tracer.start_span('set_address_filtering', child_of=request.span) as span:
            kw = controller.cleaned_data['search']
            if request.user.is_global and request.user.global_active:
                # Make sure the user can only read addresses in their Member
                addresses_in_member = set(get_addresses_in_member(request, span))
                if kw.get('address_id__in', False):
                    requested_addresses = {int(i) for i in kw['address_id__in']}
                    kw['address_id__in'] = addresses_in_member & requested_addresses
                else:
                    kw['address_id__in'] = addresses_in_member
            else:
                kw['address_id'] = request.user.address['id']

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = Category.objects.filter(
                    **kw,
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='plot_category_list_001')

        with tracer.start_span('generating_metadata', child_of=request.span):
            limit = controller.cleaned_data['limit']
            order = controller.cleaned_data['order']
            page = controller.cleaned_data['page']
            total_records = objs.count()
            warnings = controller.warnings
            metadata = {
                'limit': limit,
                'order': order,
                'page': page,
                'total_records': total_records,
                'warnings': warnings,
            }
            objs = objs[page * limit:(page + 1) * limit]

        # Serializing items and returning response
        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = CategorySerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Category record

        description: |
            Create a new Category record in the requesting User's address, using the data supplied by the User.

        responses:
            201:
                description: Category record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CategoryCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.address_id = request.user.address['id']
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CategorySerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class CategoryResource(APIView):
    """
    Handles methods regarding Category records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Category record

        description: |
            Attempt to read a Category record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Category record to be read
                type: integer

        responses:
            200:
                description: Category record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_category_object', child_of=request.span):
            try:
                obj = Category.objects.get(id=pk)
            except Category.DoesNotExist:
                return Http404(error_code='plot_category_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CategorySerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Category record
        description: |
            Attempt to update a Category record in the requesting User's address by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Category record to be updated
                type: integer

        responses:
            200:
                description: Category record was updated successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_category_object', child_of=request.span):
            try:
                obj = Category.objects.get(id=pk, address_id=request.user.address['id'])
            except Category.DoesNotExist:
                return Http404(error_code='plot_category_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CategoryUpdateController(
                data=request.data,
                instance=obj,
                partial=partial,
                request=request,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('Serializing_data', child_of=request.span):
            data = CategorySerializer(instance=controller.instance).data
        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Category record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Category record

        description: |
            Attempt to delete a Category record in the requesting User's address by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Category record to delete
                type: integer

        responses:
            204:
                description: Category record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_category_object', child_of=request.span):
            try:
                obj = Category.objects.get(id=pk, address_id=request.user.address['id'])
            except Category.DoesNotExist:
                return Http404(error_code='plot_category_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        with tracer.start_span('cascade_delete_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
