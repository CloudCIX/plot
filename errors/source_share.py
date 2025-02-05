"""
Error codes for all the methods in Source Share
"""
# List
plot_source_share_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
plot_source_share_create_101 = 'The "address_id" parameter is invalid. "address_id" is required.'
plot_source_share_create_102 = 'The "address_id" parameter is invalid. "address_id" must be an integer'
plot_source_share_create_103 = 'The "address_id" parameter is invalid. You cannot create a Share for your own Address.'

plot_source_share_create_104 = (
    'The "address_id" parameter is invalid. "address_id" must belong to a valid Address that your Address is linked to.'
)
plot_source_share_create_105 = 'The "source_id" parameter is invalid. "source_id" is required.'
plot_source_share_create_106 = 'The "source_id" parameter is invalid. "source_id" must be an integer.'
plot_source_share_create_107 = (
    'The "source_id" parameter is invalid. "source_id" must correspond to a valid Source in your Address.'
)
plot_source_share_create_108 = (
    'The "source_id" parameter is invalid. A Source Share already exists for the sent "source_id" and "address_id".'
)
plot_source_share_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
plot_source_share_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Source Share record.'
plot_source_share_read_201 = (
    'You do not have permission to execute this method. You can only read Source Share records for your address.'
)
plot_source_share_read_202 = (
    'You do not have permission to execute this method. You can only read Source Share records for Addresses in your '
    'Member.'
)

# Delete
plot_source_share_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid SourceShare record.'
