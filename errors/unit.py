"""
Error codes for all the methods in Unit
"""
# List
plot_unit_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Read
plot_unit_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Unit record.'
plot_unit_read_201 = (
    'You do not have permission to execute this method. You can only read Unit records for your address.'
)
plot_unit_read_202 = (
    'You do not have permission to execute this method. You can only read Unit records for Addresses in your Member.'
)

# Create
plot_unit_create_101 = 'The "abbreviation" parameter is invalid. "abbreviation" is required and must be a string.'
plot_unit_create_102 = 'The "abbreviation" parameter is invalid. "abbreviation" must have a value.'
plot_unit_create_103 = 'The "abbreviation" parameter is invalid. "abbreviation" cannot be longer than 50 characters.'
plot_unit_create_104 = 'The "name" parameter is invalid. "name" is required and must be a string.'
plot_unit_create_105 = 'The "name" parameter is invalid. "name" must have a value.'
plot_unit_create_106 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
plot_unit_create_107 = (
    'The "name" parameter is invalid. A Unit with the sent "name" and "abbreviation" already exists.'
)
plot_unit_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Update
plot_unit_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Unit record.'
plot_unit_update_101 = 'The "abbreviation" parameter is invalid. "abbreviation" is required and must be a string.'
plot_unit_update_102 = 'The "abbreviation" parameter is invalid. "abbreviation" must have a value.'
plot_unit_update_103 = 'The "abbreviation" parameter is invalid. "abbreviation" cannot be longer than 50 characters.'
plot_unit_update_104 = 'The "name" parameter is invalid. "name" is required and must be a string.'
plot_unit_update_105 = 'The "name" parameter is invalid. "name" must have a value.'
plot_unit_update_106 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
plot_unit_update_107 = (
    'The "name" parameter is invalid. A Unit with the sent "name" and "abbreviation" already exists.'
)

# Delete
plot_unit_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Unit record.'
plot_unit_delete_201 = (
    'You do not have permission to make this request. You cannot delete a unit that is associated with one or more '
    'Sources.'
)
