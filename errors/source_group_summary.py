"""
Error codes for all the methods in Source Group Summary
"""
# List
plot_source_group_summary_list_001 = (
    '"unit_id" is invalid. "unit_id" is required as a search filter and must be an integer.'
)
plot_source_group_summary_list_002 = '"unit_id" is invalid. "unit_id" must belong to a valid Unit record.'
plot_source_group_summary_list_003 = (
    '"start_date" and/or "end_date" are  invalid. "start_date" and "end_date" are required as a search filter must '
    'both be a date.'
)
plot_source_group_summary_list_004 = (
    '"interval" is invlaid. "interval" is required as a search filter and should start with a number for the '
    'frequency followed by a letter representing the period'
)
plot_source_group_summary_list_005 = (
    '"interval" is invlaid. "interval" should end with a letter representing the period. Supported periods are d(day), '
    'm(month), q(quarter), y(year)'
)
plot_source_group_summary_list_006 = (
    '"accumulating" is invalid. "accumulating" is required as a search filter and must be a boolean.'
)
