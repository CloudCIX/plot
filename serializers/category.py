# libs
import serpy
# local

__all__ = [
    # Category Serializer
    'CategorySerializer',
]


class CategorySerializer(serpy.Serializer):
    """
    address_id:
        description: Address ID of the Category object
        type: integer
    created:
        description: Timestamp, in ISO format, of when the Category record was created.
        type: string
    id:
        description: The ID of the Category
        type: integer
    name:
        description: The name of the category
        type: string
    updated:
        description: Timestamp, in ISO format, of when the Category record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Category instance.
        type: string
    """
    address_id = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    name = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
