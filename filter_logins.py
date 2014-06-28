#!/usr/bin/env python

from __future__ import print_function

import json
import urllib2

import dateutil.parser
from flanker.addresslib import address
from collections import OrderedDict
from contextlib import closing

APRIL_BEGIN = dateutil.parser.parse('2014-04-01T00:00:00+00:00')
MAY_BEGIN = dateutil.parser.parse('2014-05-01T00:00:00+00:00')

def in_april(datetime):
    if datetime is None:
        return False
    return APRIL_BEGIN <= datetime < MAY_BEGIN

def sort_by_date(item):
    return item['login_date']

def extract_data(json_data):
    unique_emails = OrderedDict()
    april_logins = []
    domain_counts = {}

    for login in json_data['data']:
        login_date_str = login.get('login_date')
        login_datetime = None
        if login_date_str:
            try:
                login_datetime = dateutil.parser.parse(login_date_str)
            except ValueError:
                pass
        email = login.get('email')
        if email:
            stripped_email = email.strip()
            if stripped_email:
                unique_emails[stripped_email] = True
        if in_april(login_datetime):
            april_logins.append(login)
        parsed_email = address.parse(email)
        if parsed_email is not None:
            domain = parsed_email.hostname
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
    return (unique_emails, april_logins, domain_counts)

def format_output(unique_emails, april_logins, domain_counts):
    print('# uniques')
    for email in unique_emails.iterkeys():
        print(email)
    print('# domains with > 1 user')
    for domain, count in domain_counts.iteritems():
        if count > 1:
            print((str(domain), count))
    print('# april logins')
    for login in sorted(april_logins, key=sort_by_date):
        print(json.dumps(login))

if __name__ == '__main__':
    import sys
    with closing(urllib2.urlopen(sys.argv[1])) as response:
        json_data = json.load(response)
        format_output(*extract_data(json_data))
