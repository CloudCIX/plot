"""
Management for Source Summary reports
This service displays aggregated data from the Readings of a Source. It does not create any records
"""
# stdlib
from dateutil import parser
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
# local
from plot.controllers import SourceSummaryListController
from plot.models import Reading, Source
from plot.permissions.source_summary import Permissions
from plot.utils import get_date_list


__all__ = [
    'SourceSummaryCollection',
]


class SourceSummaryCollection(APIView):
    """
    Handles methods regarding Source records which do not require an id specified
    """

    def get(self, request: Request, source_id: int) -> Response:
        """
        summary: Calculate the daily values of Readings for a specified Source for a date range

        description: Summary report of readings for source calculated based on interval in request.

        path_params:
            source_id:
                description: The ID of the Source record to summarise readings for.
                type: integer

        responses:
            200:
                description: Summary report of readings for source calculated based on interval in request.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                accumulating:
                                    description: A flag stating if the reading values are accumulating.
                                    type: boolean
                                interval:
                                    description: The interval the reading calculations were based on.
                                    type: string
                                total:
                                    description: The total value of the readings for the specified period.
                                    type: string
                                source_name:
                                    description: The name of the Source the summary is for.
                                    type: string
                                unit_name:
                                    description: The name of the unit the readings are measured in.
                                    type: string
                                unit_symbol:
                                    description: The abbreviation of the name of the unit the readings are measured in.
                                    type: string
                                values:
                                    description: The date and the summary values of the readings.
                                    type: list
                                    properties:
                                        date:
                                            type: string
                                        value:
                                            type: string
            400: {}
        """
        tracer = settings.TRACER
        with tracer.start_span('retrieving_source_object', child_of=request.span):
            try:
                source = Source.objects.get(id=source_id)
            except Source.DoesNotExist:
                return Http404(error_code='plot_source_summary_list_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.list(request, source)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            # Validate using the controller
            controller = SourceSummaryListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('validating_search_filters_sent', child_of=request.span) as span:
            search = controller.cleaned_data['search']
            try:
                start_date = parser.parse(search.get('start_date', None))
                end_date = parser.parse(search.get('end_date', None))
            except (TypeError, ValueError):
                return Http400(error_code='plot_source_summary_list_002')
            try:
                interval = search.get('interval', None)
                frequency = int(interval[:-1])
                period = interval[-1]
            except (TypeError, ValueError):
                return Http400(error_code='plot_source_summary_list_003')
            if period.lower() not in ['d', 'm', 'q', 'y']:
                return Http400(error_code='plot_source_summary_list_004')

        with tracer.start_span('creating_response_structure', child_of=request.span):
            content = {
                'accumulating': source.accumulating,
                'interval': interval,
                'total': 0,
                'source_name': source.description,
                'unit_name': source.unit.name,
                'unit_symbol': source.unit.abbreviation,
                'values': [],
            }

        with tracer.start_span('creating_date_list_for_filter', child_of=request.span):
            date_list = get_date_list(start_date, end_date, frequency, period.lower())

        with tracer.start_span('get_reading_results_per_range', child_of=request.span):
            i = 0
            interval_values = []
            while i < len(date_list) - 1:
                reading_values = Reading.objects.filter(
                    datetime_taken__gt=f'{date_list[i]} 23:59:59.999999',
                    datetime_taken__lte=f'{date_list[i+1]} 23:59:59.999999',
                    source=source,
                ).values_list('value', flat=True)
                i += 1
                if len(reading_values) == 0:
                    content['values'].append({'date': date_list[i], 'value': None})
                    continue
                if source.accumulating is True:
                    value = max(reading_values)
                else:
                    value = sum(reading_values) / len(reading_values)
                interval_values.append(value)
                content['values'].append({'date': date_list[i], 'value': value})

            if source.accumulating is True:
                content['total'] = max(interval_values, default=0)
            else:
                if interval_values:
                    content['total'] = sum(interval_values) / len(interval_values)
                else:
                    content['total'] = 0.0

        return Response({'content': content})
