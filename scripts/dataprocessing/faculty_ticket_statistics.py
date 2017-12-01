from __future__ import print_function
from collections import defaultdict
import sys
import dateparser
from tqdm import tqdm
import unicodecsv as csv

ticket_details_filename = sys.argv[1]
ticket_history_filename = sys.argv[2]

with open(ticket_details_filename, 'rb') as f:
    ticket_details = list(csv.DictReader(f))
with open(ticket_history_filename, 'rb') as f:
    ticket_history = list(csv.DictReader(f))
    
print("Rows in ticket_details (# tickets): {}".format(len(ticket_details)))
print("Rows in ticket_history: {}".format(len(ticket_history)))

# Reformat the date strings into datetime objects so we can do math on them
# Also reformat the logged time spent values so that we can do math on them
# Change the u'\ufeff"ticketID"' key into a proper u'ticketID' that's easier to access
for i, item in tqdm(enumerate(ticket_details)):
    ticket_details[i][u'dateCreated'] = dateparser.parse(item[u'dateCreated'], settings={'TIMEZONE': 'US/Central'})
    ticket_details[i][u'dateUpdated'] = dateparser.parse(item[u'dateUpdated'], settings={'TIMEZONE': 'US/Central'})
    ticket_details[i][u'ticketID'] = item.pop(u'\ufeff"ticketID"')
    try:
        ticket_details[i][u'hoursSpent'] = float(item[u'hoursSpent'])
    except:
        print("ticket_details[i][u'hoursSpent'] = {} cannot be parsed as a float. Recording as 0.".format(ticket_details[i][u'hoursSpent']))
        ticket_details[i][u'hoursSpent'] = 0.0
for i, item in tqdm(enumerate(ticket_history)):
    ticket_history[i][u'Action Date'] = dateparser.parse(item[u'Action Date'], settings={'TIMEZONE': 'US/Central'})
    ticket_history[i][u'ticketID'] = item.pop(u'\ufeff"Ticket ID"')
    try:
        ticket_history[i][u'Time Spent'] = float(item[u'Time Spent'])
    except:
        print("ticket_history[i][u'Time Spent'] = {} cannot be parsed as a float. Recording as 0.".format(ticket_history[i][u'Time Spent']))
        ticket_history[i][u'Time Spent'] = 0.0

# Clean up the ticket_details to remove all the keys with 'RETIRED' in their name
retired_keys = filter(lambda s: 'RETIRED' in s, ticket_details[0].keys())
for i, item in tqdm(enumerate(ticket_details)):
    for key in retired_keys:
        ticket_details[i].pop(key)

faculty_computing_service_families = [u'Accounts & Security',
     u'Email & Messaging',
     u'Kellogg Websites & Apps',
     u'Loaner Equipment',
     u'Network & Infrastructure',
     u'Other Business/Enterprise Services',
     u'Personal Computing',
     u'Printing']
faculty_ticket_details = filter(lambda td: td[u'Pilot/Project?'] == u'Faculty Support', ticket_details) + \
                         filter(lambda td: td[u'sla'] == u'Faculty', ticket_details) + \
                         filter(lambda td: td[u'accountName'] == u'Faculty', ticket_details)
faculty_ticket_details = filter(lambda td: td[u'Service Family'] in faculty_computing_service_families, 
                                faculty_ticket_details)
ticket_details_by_ticketid = {td[u'ticketID']: td for td in ticket_details}
ticket_history_by_ticketid = defaultdict(list)
for th in ticket_history:
    ticket_history_by_ticketid[th[u'ticketID']].append(th)
faculty_tickets = defaultdict(dict)
faculty_ticketids = set([td[u'ticketID'] for td in faculty_ticket_details])
for ticketid in faculty_ticketids:
    faculty_tickets[ticketid]['details'] = ticket_details_by_ticketid[ticketid]
    faculty_tickets[ticketid]['history'] = ticket_history_by_ticketid[ticketid]

def first_solve_date(ticketid):
    found_first_solve = False
    _first_solve_date = None
    for item in sorted(faculty_tickets[ticketid]['history'], key=lambda h: h[u'Action Date']):
        if item[u'Action Name'] == 'Solve' and not found_first_solve:
            found_first_solve = True
            _first_solve_date = item[u'Action Date']
            break
    return _first_solve_date

def last_solve_date(ticketid):
    _last_solve_date = None
    for item in sorted(faculty_tickets[ticketid]['history'], key=lambda h: h[u'Action Date']):
        if item[u'Action Name'] == 'Solve':
            _last_solve_date = item[u'Action Date']
    return _last_solve_date

# Let's restrict the tickets to only the ones that have a solution in their history
faculty_ticket_details = []
for ticketid in faculty_ticketids:
    if first_solve_date(ticketid):
        faculty_ticket_details.append(ticket_details_by_ticketid[ticketid])
    else:
        # This ticket has not been solved yet, so get rid of it
        faculty_tickets.pop(ticketid)
        
# Let's break down ticket details by customer, keying off of customerEmail
ticket_details_by_customer = defaultdict(list)
for td in faculty_ticket_details:
    email = td[u'customerEmail']
    ticket_details_by_customer[email].append(td)

# Let's get a list of customers with a count of tickets each
ticket_count_by_customer = {}
for email in ticket_details_by_customer:
    ticket_count_by_customer[email] = len(ticket_details_by_customer[email])

# Let's get a list of customers with total time spent each
ticket_time_by_customer = defaultdict(lambda: 0.0)
for email in ticket_details_by_customer:
    ticket_time_by_customer[email] = sum([td[u'hoursSpent'] for td in ticket_details_by_customer[email]])

def time_to_resolution(ticketid, resolution_type='initial', units='seconds'):
    date_created = faculty_tickets[ticketid]['details'][u'dateCreated']
    if resolution_type == 'initial':
        solution_date = first_solve_date(ticketid)
    elif resolution_type == 'final':
        solution_date = last_solve_date(ticketid)
    else:
        raise
    # In the case of tickets that have not been solved yet, we'll use dateUpdated on the ticket details
    # (Not ideal, better to restrict these tickets to ones that have been solved)
    if not solution_date:
        solution_date = faculty_tickets[ticketid]['details'][u'dateUpdated']
    _time_to_resolution = (solution_date - date_created).total_seconds()
    if units == 'minutes':
        _time_to_resolution = _time_to_resolution / 60.
    elif units == 'hours':
        _time_to_resolution = _time_to_resolution / 3600.
    elif units == 'days':
        _time_to_resolution = _time_to_resolution / (3600*24.)
    return _time_to_resolution

for customer, tds in ticket_details_by_customer.iteritems():
    for i, td in enumerate(tds):
        ticket_details_by_customer[customer][i]['ttir_seconds'] = time_to_resolution(td[u'ticketID'], 'initial', 'seconds')
        ticket_details_by_customer[customer][i]['ttfr_seconds'] = time_to_resolution(td[u'ticketID'], 'final', 'seconds')

# Let's get a list of customers with total time to resolution (initial, final) each
total_initial_time_to_resolution_by_customer = {}
total_final_time_to_resolution_by_customer = {}
for email, tds in ticket_details_by_customer.iteritems():
    total_initial_time_to_resolution_by_customer[email] = sum([td[u'ttir_seconds'] for td in tds])
    total_final_time_to_resolution_by_customer[email] = sum([td[u'ttfr_seconds'] for td in tds])

print("Total Initial Time (first solve) to Resolution:")
for customer, total_time in sorted(total_initial_time_to_resolution_by_customer.items(), key=lambda n: n[1], reverse=True):
    total_time_hours = total_time / 3600.
    avg = total_time_hours / ticket_count_by_customer[customer]
    print("{0}: {1} hours (avg: {2})".format(customer, total_time_hours, avg))
print("Total Final Time (last solve) to Resolution:")
for customer, total_time in sorted(total_final_time_to_resolution_by_customer.items(), key=lambda n: n[1], reverse=True):
    total_time_hours = total_time / 3600.
    avg = total_time_hours / ticket_count_by_customer[customer]
    print("{0}: {1} hours (avg: {2})".format(customer, total_time_hours, avg))

for customer, total_time in sorted(ticket_time_by_customer.items(), key=lambda n: n[1], reverse=True):
    total_ttir_hours = total_initial_time_to_resolution_by_customer[customer] / (3600.)
    total_ttfr_hours = total_final_time_to_resolution_by_customer[customer] / (3600.)
    print("{0} Total time spent: {1} Total time to initial res.: {2} Total time to final res.: {3}".format(
            customer, total_time, total_ttir_hours, total_ttfr_hours))
    
# ticket_details_by_customer (keys are emails, values are lists of ticket_detail dicts)
# ticket_count_by_customer (keys are emails, values are integer counts of tickets in hours)
# ticket_time_by_customer (keys are emails, values are float total time spent per customer in hours)
# total_initial_time_to_resolution_by_customer (keys are emails, values are float total time to initial resolution per customer in seconds)
# total_final_time_to_resolution_by_customer (keys are emails, values are float total time to final resolution per customer in seconds)
# TODO
# total_escalations_by_customer (keys are emails, values are integer counts of total escalations that occur in tickets per customer)
# total_history_items_by_customer (keys are emails, values are integer counts of total ticket history items per customer)
# per ticket, count number of unique CSRs that interacted with it in the history
# 
