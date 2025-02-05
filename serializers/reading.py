# libs
import serpy
# local
from .source import SourceSerializer

__all__ = [
    # Reading Serializer
    'ReadingSerializer',
]


class ReadingSerializer(serpy.Serializer):
    """
    datetime_taken:
        description: Date and time that a reading was taken
        type: string
    id:
        description: The ID of the Reading
        type: integer
    source:
        $ref: '#/components/schemas/Source'
    source_id:
        description: The ID of the Source of the Reading
        type: integer
    uri:
        description: URL that can be used to run methods in the API associated with the Reading instance.
        type: string
    value:
        description: value of the Readings
        type: string
        format: decimal
    """
    datetime_taken = serpy.Field(attr='datetime_taken.isoformat', call=True)
    id = serpy.Field()
    source = SourceSerializer()
    source_id = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)
    value = serpy.StrField()
