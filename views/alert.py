"""
Management of Alert service
"""
# libs
from cloudcix_rest.views import APIView
from django.conf import settings
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
# local
from ..models import Reading
from ..serializers import ReadingSerializer
from plot.utils import get_addresses_in_member


class AlertCollection(APIView):
    """
    Handles the view for list of Red and Amber alerts.
    """
    def get(self, request: Request) -> Response:
        """
        summary: Get the list of Red and Amber alerts.

        description: |
            Based on the latest Reading for each source, determines if it is a red or amber alert to return in
            response.

        responses:
            200:
                description: A list of Red and Amber alerts are returned successfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                amber_high_alerts:
                                    $ref: '#/components/schemas/Reading'
                                amber_low_alerts:
                                    $ref: '#/components/schemas/Reading'
                                green_alerts:
                                    $ref: '#/components/schemas/Reading'
                                red_high_alerts:
                                    $ref: '#/components/schemas/Reading'
                                red_low_alerts:
                                   $ref: '#/components/schemas/Reading'

        """
        tracer = settings.TRACER

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

        with tracer.start_span('get_reading_objects', child_of=request.span):
            readings = Reading.objects.filter(
                address_filtering,
                source__deleted__isnull=True,
            ).order_by('source_id', '-datetime_taken').distinct('source_id')

        with tracer.start_span('compare values', child_of=request.span):
            amber_high_alerts, amber_low_alerts, green_alerts, red_high_alerts, red_low_alerts = [], [], [], [], []
            for reading in readings:
                if not reading.source.accumulating:
                    if reading.value <= reading.source.red_low:
                        red_low_alerts.append(reading)
                    elif reading.value >= reading.source.red_high:
                        red_high_alerts.append(reading)
                    elif reading.value <= reading.source.amber_low:
                        amber_low_alerts.append(reading)
                    elif reading.value >= reading.source.amber_high:
                        amber_high_alerts.append(reading)
                    else:
                        green_alerts.append(reading)

            alerts = [
                amber_high_alerts,
                amber_low_alerts,
                green_alerts,
                red_high_alerts,
                red_low_alerts,
            ]
            for item in alerts:
                item.sort(key=lambda x: x.datetime_taken, reverse=True)

        with tracer.start_span('get_data', child_of=request.span):
            data = {
                'amber_high_alerts': ReadingSerializer(instance=amber_high_alerts, many=True).data,
                'amber_low_alerts': ReadingSerializer(instance=amber_low_alerts, many=True).data,
                'green_alerts': ReadingSerializer(instance=green_alerts, many=True).data,
                'red_high_alerts': ReadingSerializer(instance=red_high_alerts, many=True).data,
                'red_low_alerts': ReadingSerializer(instance=red_low_alerts, many=True).data,
            }

        return Response({'content': data})
