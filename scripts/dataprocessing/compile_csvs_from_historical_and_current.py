#!/usr/bin/python
import glob
import unicodecsv as csv
import sys

DATESTRING = sys.argv[1]

details_csv_filenames = glob.glob('historical/noBOM/ticket_details*.csv') + glob.glob('current/noBOM/ticket_details_{0}*.csv'.format(DATESTRING))
history_csv_filenames = glob.glob('historical/noBOM/ticket_history*.csv') + glob.glob('current/noBOM/ticket_history_{0}*.csv'.format(DATESTRING))

details = []
history = []
for details_csv_filename in details_csv_filenames:
    print "Reading in " + details_csv_filename
    with open(details_csv_filename, 'rb') as f:
        details += list(csv.DictReader(f))
for history_csv_filename in history_csv_filenames:
    print "Reading in " + history_csv_filename
    with open(history_csv_filename, 'rb') as f:
        history += list(csv.DictReader(f))

print "Writing out ticket_details"
with open('compiled/ticket_details_{0}-noBOM.csv'.format(DATESTRING), 'wb') as f:
    fieldnames = sorted(details[0].keys())
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(details)
print "Writing out ticket_history"
with open('compiled/ticket_history_{0}-noBOM.csv'.format(DATESTRING), 'wb') as f:
    fieldnames = sorted(history[0].keys())
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(history)

