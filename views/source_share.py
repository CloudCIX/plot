"""
Management of Source Shares
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
    SourceShareListController,
    SourceShareCreateController,
)
from plot.models import SourceShare
from plot.permissions.source_share import Permissions
from plot.serializers import SourceShareSerializer
from plot.utils import get_addresses_in_member

__all__ = [
    'SourceShareCollection',
    'SourceShareResource',
]


class SourceShareCollection(APIView):
    """
    Handles methods regarding Source Share records that do not require an id to be specified, i.e. list
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Source Share records

        description: |
            Retrieve a list of the Source Share records for the requesting User's Member.

        responses:
            200:
                description: A list of the Source Share records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        # validating controller
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = SourceShareListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('set_address_filtering', child_of=request.span) as span:
            addresses = [request.user.address['id']]
            if request.user.is_global and request.user.global_active:
                addresses = get_addresses_in_member(request, span)
            # List readings for Sources where address is in Category or Source Share
            address_filtering = Q(
                source__category__address_id__in=addresses,
            )

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = SourceShare.objects.filter(
                    address_filtering,
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='plot_source_share_list_001')

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
            data = SourceShareSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Source Share record

        description: |
            Create a new Source Share record in the requesting Users Address, using the data supplied by the User.

        responses:
            201:
                description: Source Share record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = SourceShareCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = SourceShareSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class SourceShareResource(APIView):
    """
    Handles methods regarding Source Share records that do require an id to be specified, i.e. read
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Source Share record

        description: |
            Attempt to read a Source Share record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Source Share record to be read
                type: integer

        responses:
            200:
                description: Source Share record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_source_share_object', child_of=request.span):
            try:
                obj = SourceShare.objects.get(id=pk)
            except SourceShare.DoesNotExist:
                return Http404(error_code='plot_source_share_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = SourceShareSerializer(instance=obj).data

        return Response({'content': data})

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified SourceShare record

        description: |
            Attempt to delete a SourceShare record in the requesting User's address by the given 'pk',
            returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the SourceShare record to delete
                type: integer

        responses:
            204:
                description: SourceShare record was deleted successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_source_share_object', child_of=request.span):
            try:
                obj = SourceShare.objects.get(id=pk, source__category__address_id=request.user.address['id'])
            except SourceShare.DoesNotExist:
                return Http404(error_code='plot_source_share_delete_001')

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
