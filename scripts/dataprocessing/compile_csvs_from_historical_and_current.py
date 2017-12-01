#!/usr/bin/python
import glob
import unicodecsv as csv

details_csv_filenames = glob.glob('historical/noBOM/ticket_details*.csv') + glob.glob('current/noBOM/ticket_details*.csv')
history_csv_filenames = glob.glob('historical/noBOM/ticket_history*.csv') + glob.glob('current/noBOM/ticket_history*.csv')

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
with open('compiled/ticket_details_20171121-noBOM.csv', 'wb') as f:
    fieldnames = sorted(details[0].keys())
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(details)
print "Writing out ticket_history"
with open('compiled/ticket_history_20171121-noBOM.csv', 'wb') as f:
    fieldnames = sorted(history[0].keys())
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(history)

