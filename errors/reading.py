"""
Error codes for all the methods in Reading
"""
# List
plot_reading_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create

plot_reading_create_101 = 'The "source_id" parameter is invalid. "source_id" is required.'
plot_reading_create_102 = 'The "source_id" parameter is invalid. "source_id" must be an integer.'
plot_reading_create_103 = (
    'The "source_id" parameter is invalid. "source_id" must correspond to a valid Source in your Address.'
)
plot_reading_create_104 = (
    'The "datetime_taken" parameter is invalid. "datetime_taken" is required and should be a date timestamp in the '
    'format of yyyy-mm-ddThh:mm:ss'
)
plot_reading_create_105 = (
    'The "datetime_taken" parameter is invalid. "datetime_taken" must be be for a date and time in the past.'
)
plot_reading_create_106 = (
    'The "datetime_taken" parameter is invalid. A Reading with this time already exists for the sent Source.'
)
plot_reading_create_107 = 'The "value" parameter is invalid. "value" is a required field.'
plot_reading_create_108 = 'The "value" parameter is invalid. "value" must be a string in decimal format.'
plot_reading_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
plot_reading_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Reading record.'

# Update
plot_reading_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Reading record.'
plot_reading_update_201 = (
    'You do not have permission to execute this method. Only Administrators can update a Reading record.'
)
plot_reading_update_101 = (
    'The "datetime_taken" parameter is invalid. "datetime_taken" is required and should be a date timestamp in the '
    'format of yyyy-mm-ddThh:mm:ss'
)
plot_reading_update_102 = (
    'The "datetime_taken" parameter is invalid. "datetime_taken" must be be for a date and time in the past.'
)
plot_reading_update_103 = (
    'The "datetime_taken" parameter is invalid. A Reading with this time already exists for this Source.'
)
plot_reading_update_104 = 'The "value" parameter is invalid. "value" is a required field.'
plot_reading_update_105 = 'The "value" parameter is invalid. "value" must be a string in decimal format.'

# Delete
plot_reading_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Reading record.'
plot_reading_delete_201 = (
    'You do not have permission to execute this method. Only Administrators can delete a Reading record.'
)
