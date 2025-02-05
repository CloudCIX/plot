"""
Error codes for all the methods in Source
"""
# List
plot_source_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
plot_source_create_101 = 'The "accumulating" parameter is invalid. "accumulating" must be a boolean'
plot_source_create_102 = 'The "category_id" parameter is invalid. "category_id" is required.'
plot_source_create_103 = 'The "category_id" parameter is invalid. "category_id" must be an integer.'
plot_source_create_104 = (
    'The "category_id" parameter is invalid. "category_id" must correspond to a valid Category in your Address.'
)
plot_source_create_105 = 'The "description" parameter is invalid. "description" is required and must be a string.'
plot_source_create_106 = 'The "description" parameter is invalid. "description" cannot be longer than 50 characters.'
plot_source_create_107 = (
    'The "description" parameter is invalid. "description" is already in use for another Source within this Category.'
)
plot_source_create_108 = 'The "seconds_valid" parameter is invalid. "seconds_valid" is required and must be an integer.'
plot_source_create_109 = 'The "seconds_valid" parameter is invalid. "seconds_valid" must be an integer.'
plot_source_create_110 = 'The "seconds_valid" parameter is invalid. "seconds_valid" must be greater than 0.'
plot_source_create_111 = 'The "unit_id" parameter is invalid. "unit_id" is required.'
plot_source_create_112 = 'The "unit_id" parameter is invalid. "unit_id" must be an integer.'
plot_source_create_113 = (
    'The "unit_id" parameter is invalid. "unit_id" must correspond to a valid Unit in your Address.'
)
plot_source_create_114 = (
    'The "red_high" parameter is invalid. "red_high" is required and must be a string in decimal format.'
)
plot_source_create_115 = (
    'The "amber_high" parameter is invalid. "amber_high" is required and must be a string in decimal format.'
)
plot_source_create_116 = (
    'The "amber_high" parameter is invalid. "amber_high" must be less than the value for "red_high".'
)
plot_source_create_117 = (
    'The "amber_low" parameter is invalid. "amber_low" is required and must be a string in decimal format.'
)
plot_source_create_118 = (
    'The "amber_low" parameter is invalid. "amber_low" must be less than the value for "amber_high".'
)
plot_source_create_119 = (
    'The "red_low" parameter is invalid. "red_low" is required and must be a string in decimal format.'
)
plot_source_create_120 = 'The "red_low" parameter is invalid. "red_low" must be less than the value for "amber_low".'
plot_source_create_121 = 'The "retention" parameter is invalid. "retention" must be an integer.'
plot_source_create_122 = 'The "retention" parameter is invalid. "retention" must be greater than 0.'

# Read
plot_source_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Source record.'
plot_source_read_201 = (
    'You do not have permission to execute this method. You can only read Source records for your Address.'
)
plot_source_read_202 = (
    'You do not have permission to execute this method. You can only read Source records for Addresses in your '
    'Member.'
)

# Update
plot_source_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Source record.'
plot_source_update_101 = 'The "accumulating" parameter is invalid. "accumulating" must be a boolean'
plot_source_update_102 = 'The "category_id" parameter is invalid. "category_id" is required.'
plot_source_update_103 = 'The "category_id" parameter is invalid. "category_id" must be an integer.'
plot_source_update_104 = (
    'The "category_id" parameter is invalid. "category_id" must correspond to a valid Category in your Address.'
)
plot_source_update_105 = 'The "description" parameter is invalid. "description" is required and must be a string.'
plot_source_update_106 = 'The "description" parameter is invalid. "description" cannot be longer than 50 characters.'
plot_source_update_107 = (
    'The "description" parameter is invalid. "description" is already in use for another Source within this Category.'
)
plot_source_update_108 = 'The "seconds_valid" parameter is invalid. "seconds_valid" is required and must be an integer.'
plot_source_update_109 = 'The "seconds_valid" parameter is invalid. "seconds_valid" must be an integer.'
plot_source_update_110 = 'The "seconds_valid" parameter is invalid. "seconds_valid" must be greater than 0.'
plot_source_update_111 = 'The "unit_id" parameter is invalid. "unit_id" is required.'
plot_source_update_112 = 'The "unit_id" parameter is invalid. "unit_id" must be an integer.'
plot_source_update_113 = (
    'The "unit_id" parameter is invalid. "unit_id" must correspond to a valid Unit in your Address.'
)
plot_source_update_114 = (
    'The "red_high" parameter is invalid. "red_high" is required and must be a string in decimal format.'
)
plot_source_update_115 = (
    'The "amber_high" parameter is invalid. "amber_high" is required and must be a string in decimal format.'
)
plot_source_update_116 = (
    'The "amber_high" parameter is invalid. "amber_high" must be less than the value for "red_high".'
)
plot_source_update_117 = (
    'The "amber_low" parameter is invalid. "amber_low" is required and must be a string in decimal format.'
)
plot_source_update_118 = (
    'The "amber_low" parameter is invalid. "amber_low" must be less than the value for "amber_high".'
)
plot_source_update_119 = (
    'The "red_low" parameter is invalid. "red_low" is required and must be a string in decimal format.'
)
plot_source_update_120 = 'The "red_low" parameter is invalid. "red_low" must be less than the value for "amber_low".'
plot_source_update_121 = 'The "retention" parameter is invalid. "retention" must be an integer.'
plot_source_update_122 = 'The "retention" parameter is invalid. "retention" must be greater than 0.'

# Delete
plot_source_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Source record.'
