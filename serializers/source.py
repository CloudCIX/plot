# libs
import serpy
# local
from .category import CategorySerializer
from .unit import UnitSerializer

__all__ = [
    # Source Serializer
    'SourceSerializer',
]


class SourceSerializer(serpy.Serializer):
    """
    accumulating:
        description: A flag to state if the Readings of the Source is accumulating.
        type: boolean
    amber_high:
        description: An upper limit on normal reading values. A reading higher than the source's AmberHigh is abnormal.
        type: string
        format: decimal
    amber_low:
        description: A lower limit on normal reading values. Any reading lower than the source's Amber Low is abnormal
        type: string
        format: decimal
    category:
        $ref: '#/components/schemas/Category'
    category_id:
        description: The ID of the Category of the Source
        type: integer
    created:
        description: Timestamp, in ISO format, of when the Source record was created.
        type: string
    description:
        description: Describes the sources
        type: string
    id:
        description: The ID of the Source
        type: integer
    red_high:
        description: An upper limit on safe reading values. Any reading higher than the source's Red High is critical
        type: string
        format: decimal
    red_low:
        description: A lower limit on safe reading values. Any reading lower than the source's Red Low is critical
        type: string
        format: decimal
    retention:
        description: |
            The number of days that the Readings for the Source will be retained. Default is for 3650 days (10 years).
        type: integer
    seconds_valid:
        description: Number of seconds the reading is valid for
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Source record was last updated.
        type: string
    unit:
        $ref: '#/components/schemas/Unit'
    unit_id:
        description: The ID of the Unit of the Source
        type: integer
    uri:
        description: URL that can be used to run methods in the API associated with the Source instance.
        type: string
    """
    accumulating = serpy.Field()
    amber_high = serpy.StrField()
    amber_low = serpy.StrField()
    category = CategorySerializer()
    category_id = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    description = serpy.Field()
    id = serpy.Field()
    red_high = serpy.StrField()
    red_low = serpy.StrField()
    retention = serpy.Field()
    seconds_valid = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    unit = UnitSerializer()
    unit_id = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)
