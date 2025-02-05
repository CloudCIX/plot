"""
Error codes for all the methods in Category
"""
# List
plot_category_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Read
plot_category_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Category record.'
plot_category_read_201 = (
    'You do not have permission to execute this method. You can only read Category records for your address.'
)
plot_category_read_202 = (
    'You do not have permission to execute this method. You can only read Category records for Addresses in your '
    'Member.'
)

# Create
plot_category_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
plot_category_create_102 = 'The "name" parameter is invalid. "name" must have a value.'
plot_category_create_103 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
plot_category_create_104 = 'The "name" parameter is invalid. A Category with that name already exists.'
plot_category_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Update
plot_category_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Category record.'
plot_category_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
plot_category_update_102 = 'The "name" parameter is invalid. "name" must have a value.'
plot_category_update_103 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
plot_category_update_104 = 'The "name" parameter is invalid. A Category with that name already exists.'

# Delete
plot_category_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Category record.'
plot_category_delete_201 = (
    'You do not have permission to make this request. You cannot delete a Category that is associated with '
    'one or more Sources.'
)
