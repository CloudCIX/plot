"""
Management for Source Group Summary reports
This service displays aggregated data from the Readings of Sources. It does not create any records
"""
# stdlib
from dateutil import parser
# libs
from cloudcix_rest.exceptions import Http400
from cloudcix_rest.views import APIView
from django.conf import settings
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
# local
from plot.controllers import SourceGroupSummaryListController
from plot.models import Reading, Source, Unit
from plot.utils import get_addresses_in_member, get_date_list


__all__ = [
    'SourceGroupSummaryCollection',
]


class SourceGroupSummaryCollection(APIView):
    """
    Handles methods regarding records which do not require an id specified
    """

    def get(self, request: Request, source: str) -> Response:
        """
        summary: Calculate the daily values of Readings for a Source Group for a date range

        description: Summary report of readings for a Source Group calculated based on interval in request.

        path_params:
            source:
                description: The description for Sources to summarise readings for.
                type: string

        responses:
            200:
                description: Summary report of readings for Source Group calculated based on interval in request.
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
                                    description: The description of the Sources the summary is for.
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

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            # Validate using the controller
            controller = SourceGroupSummaryListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('validating_search_filters_sent', child_of=request.span) as span:
            search = controller.cleaned_data['search']
            try:
                unit_id = int(search.get('unit_id', None))
                unit = Unit.objects.get(pk=unit_id)
            except (TypeError, ValueError):
                return Http400(error_code='plot_source_group_summary_list_001')
            except Unit.DoesNotExist:
                return Http400(error_code='plot_source_group_summary_list_002')
            try:
                start_date = parser.parse(search.pop('start_date', None))
                end_date = parser.parse(search.pop('end_date', None))
            except (TypeError, ValueError):
                return Http400(error_code='plot_source_group_summary_list_003')
            try:
                interval = search.pop('interval', None)
                frequency = int(interval[:-1])
                period = interval[-1]
            except (TypeError, ValueError):
                return Http400(error_code='plot_source_group_summary_list_004')
            if period.lower() not in ['d', 'm', 'q', 'y']:
                return Http400(error_code='plot_source_group_summary_list_005')
            accumulating = search.get('accumulating', None)
            if not isinstance(accumulating, bool):
                return Http400(error_code='plot_source_group_summary_list_006')

        # setting address filter
        with tracer.start_span('set_address_filtering', child_of=request.span) as span:
            addresses = [request.user.address['id']]
            if request.user.is_global and request.user.global_active:
                addresses = get_addresses_in_member(request, span)
            address_filtering = Q(unit__address_id__in=addresses) | Q(shares__address_id__in=addresses)

        with tracer.start_span('get_source_ids', child_of=request.span):
            sources = Source.objects.filter(
                address_filtering,
                description__icontains=source,
                **controller.cleaned_data['search'],
            ).values_list('pk', flat=True)

        with tracer.start_span('creating_response_structure', child_of=request.span):
            content = {
                'accumulating': accumulating,
                'interval': interval,
                'total': 0,
                'min_total': 0,
                'avg_total': 0,
                'max_total': 0,
                'source_name': source,
                'unit_name': unit.name,
                'unit_symbol': unit.abbreviation,
                'values': [],
            }

        with tracer.start_span('creating_date_list_for_filter', child_of=request.span):
            date_list = get_date_list(start_date, end_date, frequency, period.lower())

        with tracer.start_span('get_reading_results_per_range', child_of=request.span):
            # Logic not correct - need to think more on loop for item in date list
            interval_values = []
            min_values = []
            avg_values = []
            max_values = []
            for i in range(0, len(date_list) - 1):
                if accumulating:
                    for source in sources:
                        reading_values = Reading.objects.filter(
                            datetime_taken__gt=f'{date_list[i]} 23:59:59.999999',
                            datetime_taken__lte=f'{date_list[i + 1]} 23:59:59.999999',
                            source_id=source,
                        ).values_list('value', flat=True)
                        if len(reading_values) == 0:
                            content['values'].append(
                                {'date': date_list[i + 1], 'value': None, 'min_value': None, 'avg_value': None,
                                 'max_value': None},
                            )
                            continue

                        value = max(reading_values)
                        interval_values.append(value)
                        content['values'].append(
                            {
                                'date': date_list[i + 1],
                                'value': value,
                                'min_value': None,
                                'avg_value': None,
                                'max_value': None,
                            },
                        )
                else:
                    reading_values = Reading.objects.filter(
                        datetime_taken__gt=f'{date_list[i]} 23:59:59.999999',
                        datetime_taken__lte=f'{date_list[i + 1]} 23:59:59.999999',
                        source_id__in=sources,
                    ).values_list('value', flat=True)
                    if len(reading_values) == 0:
                        content['values'].append(
                            {'date': date_list[i + 1], 'value': None, 'min_value': None, 'avg_value': None,
                             'max_value': None},
                        )
                        continue
                    min_value = min(reading_values)
                    avg_value = sum(reading_values) / len(reading_values)
                    max_value = max(reading_values)
                    min_values.append(min_value)
                    avg_values.append(avg_value)
                    max_values.append(max_value)
                    content['values'].append(
                        {
                            'date': date_list[i + 1],
                            'value': None,
                            'min_value': min_value,
                            'avg_value': avg_value,
                            'max_value': max_value,
                        },
                    )
            if accumulating:
                content['total'] = max(interval_values, default=0)
                content['min_total'] = None
                content['avg_total'] = None
                content['max_total'] = None
            else:
                content['total'] = None
                content['min_total'] = min(min_values, default=0)
                content['max_total'] = max(max_values, default=0)
                if avg_values:
                    content['avg_total'] = sum(avg_values) / len(avg_values)
                else:
                    content['avg_total'] = 0
        return Response({'content': content})
