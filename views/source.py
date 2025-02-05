"""
Management of Sources
"""
# stdlib
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
    SourceCreateController,
    SourceListController,
    SourceUpdateController,
)
from plot.models import Source
from plot.permissions.source import Permissions
from plot.serializers import SourceSerializer
from plot.utils import get_addresses_in_member


__all__ = [
    'SourceCollection',
    'SourceResource',
]


class SourceCollection(APIView):
    """
    Handles methods regarding Source records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Source records

        description: |
            Retrieve a list of the Source records for the requesting User.

        responses:
            200:
                description: A list of the source records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        # validating controller
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = SourceListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        # setting address filter
        with tracer.start_span('set_address_filtering', child_of=request.span) as span:
            addresses = [request.user.address['id']]
            if request.user.is_global and request.user.global_active:
                addresses = get_addresses_in_member(request, span)
            address_filtering = Q(category__address_id__in=addresses) | Q(shares__address_id__in=addresses)

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = Source.objects.filter(
                    address_filtering,
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='plot_source_list_001')

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
            data = SourceSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Source record

        description: |
            Create a new Source record in the requesting Users Address, using the data supplied by the User.

        responses:
            201:
                description: Reading record was created successfully
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = SourceCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.address_id = request.user.address['id']
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = SourceSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class SourceResource(APIView):
    """
    Handles methods regarding Source records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Source record

        description: |
            Attempt to read a Source record by the given 'pk', returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Source record to be read
                type: integer

        responses:
            200:
                description: Source record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_source_object', child_of=request.span):
            try:
                obj = Source.objects.get(id=pk)
            except Source.DoesNotExist:
                return Http404(error_code='plot_source_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = SourceSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial=False) -> Response:
        """
        summary: Update the details of a specified Source record

        description: |
            Attempt to update a Source record by the given `id`, returning a 404 if it doesn't exist

        path_params:
            pk:
                description: The id of the Source to be updated
                type: integer

        responses:
            200:
                description: Source record was updated successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Source.objects.get(
                    id=pk,
                    category__address_id=request.user.address['id'],
                )
            except Source.DoesNotExist:
                return Http404(error_code='plot_source_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = SourceUpdateController(
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
            data = SourceSerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Source record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int) -> Response:
        """
        summary: Delete a specified Source record

        description: |
            Attempt to delete a Source record by the given `id`, returning a 404 if it doesn't exist

        path_params:
            pk:
                description: The id of the Source to be deleted
                type: string

        responses:
            204:
                description: Source record was deleted successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Source.objects.get(
                    id=pk,
                    category__address_id=request.user.address['id'],
                )
            except Source.DoesNotExist:
                return Http404(error_code='plot_source_delete_001')

        with tracer.start_span('saving_object', child_of=request.span):
            obj.cascade_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
