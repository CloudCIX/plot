# stdlib
from typing import List
# libs
from cloudcix.api.membership import Membership
from dateutil.relativedelta import relativedelta
from jaeger_client import Span
from rest_framework.request import Request
# local


def get_addresses_in_member(request: Request, span: Span) -> List[int]:
    """
    Given a token, make requests to Membership to fetch all the Addresses in the Member that the token is from
    """
    params = {
        'page': 0,
        'limit': 50,
        'search[member_id]': request.user.member['id'],
    }
    response = Membership.address.list(
        token=request.user.token,
        params=params,
        span=span,
    )
    if response.status_code == 200:
        address_ids = [a['id'] for a in response.json()['content']]
        total_records = response.json()['_metadata']['total_records']
        while len(address_ids) < total_records:  # pragma: no cover
            params['page'] += 1
            response = Membership.address.list(
                token=request.user.token,
                params=params,
                span=span,
            )
            address_ids.extend([a['id'] for a in response.json()['content']])
    else:  # no pragma
        address_ids = [request.user.address_id]

    return address_ids


def get_date_list(start_date, end_date, frequency, period):
    date_list = []
    # As filter uses `gt`, use previous day as first in the list
    curr_date = start_date - relativedelta(days=1)
    if period == 'd':
        # day
        while curr_date < end_date:
            date_list.append(str(curr_date.date()))
            curr_date += relativedelta(days=frequency)
    elif period == 'm':
        # month
        while curr_date < end_date:
            date_list.append(str(curr_date.date()))
            curr_date += relativedelta(day=31, months=+frequency)
    elif period == 'q':
        # quarter
        while curr_date < end_date:
            date_list.append(str(curr_date.date()))
            curr_date += relativedelta(day=31, months=+3 * frequency)
    else:
        # year
        while curr_date < end_date:
            date_list.append(str(curr_date.date()))
            curr_date += relativedelta(day=31, month=12, years=+frequency)

    date_list.append(str(end_date.date()))

    return date_list
