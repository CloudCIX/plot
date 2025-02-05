# libs
import serpy
# local

__all__ = [
    # Unit Serializer
    'UnitSerializer',
]


class UnitSerializer(serpy.Serializer):
    """
    abbreviation:
        description: Abbreviation of the Unit
        type: string
    address_id:
        description: Address ID of the Unit object
        type: integer
    created:
        description: Timestamp, in ISO format, of when the Unit record was created.
        type: string
    id:
        description: The ID of the Unit
        type: integer
    name:
        description: name of the units
        type: string
    updated:
        description: Timestamp, in ISO format, of when the Unit record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Unit instance.
        type: string
    """
    abbreviation = serpy.Field()
    address_id = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    name = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
