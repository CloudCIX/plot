# libs
import serpy
# local
from .source import SourceSerializer

__all__ = [
    'SourceShareSerializer',
]


class SourceShareSerializer(serpy.Serializer):
    """
    address_id:
        description: The Address that can view the Readings for the specified Source
        type: integer
    created:
        description: Timestamp, in ISO format, of when the SourceShare record was created.
        type: string
    id:
        description: The ID of the SourceShare object
        type: integer
    source:
        $ref: '#/components/schemas/Source'
    source_id:
        description: The ID of the Source of the Reading
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the SourceShare record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the SourceShare instance.
        type: string
    """
    address_id = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    source = SourceSerializer()
    source_id = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
