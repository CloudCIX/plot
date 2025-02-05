"""
error codes for all the methods in Source Summary
"""
# List
plot_source_summary_list_001 = (
    'The "source_id" path parameter is invalid. "source_id" must belong to a valid Source record.'
)
plot_source_summary_list_002 = (
    '"start_date" and/or "end_date" are  invalid. "start_date" and "end_date" must both be a date.'
)
plot_source_summary_list_003 = (
    '"interval" is invlaid. "interval" should start with a number for the frequency followed by a letter representing '
    'the period'
)
plot_source_summary_list_004 = (
    '"interval" is invlaid. "interval" should end with a letter representing the period. Supported periods are d(day), '
    'm(month), q(quarter), y(year)'
)
plot_source_summary_list_201 = (
    'You do not have permission to execute this method. You can only get a Source Summary for Sources in your Address'
    ' or those shared with your Address'
)
plot_source_summary_list_202 = (
    'You do not have permission to execute this method. You can only get a Source Summary for Sources for Addresses in'
    ' your Member or those shared with your Addresses in your Member.'
)
