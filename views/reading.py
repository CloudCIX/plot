"""
Management of Readings
"""
# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from plot.controllers import (
    ReadingCreateController,
    ReadingListController,
    ReadingUpdateController,
)
from plot.models import Reading
from plot.permissions.reading import Permissions
from plot.serializers import ReadingSerializer
from plot.utils import get_addresses_in_member


__all__ = [
    'ReadingCollection',
    'ReadingResource',
]


class ReadingCollection(APIView):
    """
    Handles methods regarding Reading records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Reading records

        description: |
            Retrieve a list of the Reading records from Sources and Shared Sources for the user.

        responses:
            200:
                description: A list of the Reading records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ReadingListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('set_address_filtering', child_of=request.span) as span:
            addresses = [request.user.address['id']]
            if request.user.is_global and request.user.global_active:
                addresses = get_addresses_in_member(request, span)
            # List readings for Sources where address is in Category or Source Share
            address_filtering = Q(
                source__category__address_id__in=addresses,
            ) | Q(
                source__shares__address_id__in=addresses,
            )

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = Reading.objects.filter(
                    address_filtering,
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='plot_reading_list_001')

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
            data = ReadingSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Reading record

        description: |
            Create a new Reading record for a Source using the data supplied by the User.

        responses:
            201:
                description: Reading record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ReadingCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ReadingSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class ReadingResource(APIView):
    """
    Handles methods regarding Reading records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Reading record

        description: |
            Attempt to read a Reading record by the given 'pk', returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Reading record to be read
                type: integer

        responses:
            200:
                description: Reading record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_reading_object', child_of=request.span):
            try:
                obj = Reading.objects.get(
                    id=pk,
                    source__category__address_id=request.user.address['id'],
                )
            except Reading.DoesNotExist:
                return Http404(error_code='plot_reading_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ReadingSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial=False) -> Response:
        """
        summary: Update the details of a specified Reading record

        description: |
            Attempt to update a Reading record by the given `id`, returning a 404 if it doesn't exist

        path_params:
            pk:
                description: The id of the Reading to be updated
                type: integer

        responses:
            200:
                description: Reading record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Reading.objects.get(
                    id=pk,
                    source__category__address_id=request.user.address['id'],
                )
            except Reading.DoesNotExist:
                return Http404(error_code='plot_reading_update_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ReadingUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                span=span,
                partial=partial,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ReadingSerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Reading record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int) -> Response:
        """
        summary: Delete a specified Reading record

        description: |
            Attempt to delete a Reading record by the given `id`, returning a 404 if it doesn't exist

        path_params:
            pk:
                description: The id of the Reading to be deleted
                type: string

        responses:
            204:
                description: Reading record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Reading.objects.get(
                    id=pk,
                    source__category__address_id=request.user.address['id'],
                )
            except Reading.DoesNotExist:
                return Http404(error_code='plot_reading_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request)
            if err is not None:
                return err

        with tracer.start_span('saving_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
