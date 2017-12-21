#!/usr/bin/python
from __future__ import print_function
import glob
import unicodecsv as csv
import os
import sys

DATESTRING = sys.argv[1]
HISTORICAL_FOLDER = sys.argv[2]
CURRENT_FOLDER = sys.argv[3]
COMPILED_FOLDER = sys.argv[4]

details_csv_filenames = glob.glob(HISTORICAL_FOLDER + '/noBOM/ticket_details*.csv') + \
                        glob.glob(CURRENT_FOLDER + '/noBOM/ticket_details_{0}*.csv'.format(DATESTRING))
history_csv_filenames = glob.glob(HISTORICAL_FOLDER + '/noBOM/ticket_history*.csv') + \
                        glob.glob(CURRENT_FOLDER + '/noBOM/ticket_history_{0}*.csv'.format(DATESTRING))
details_output_filename = os.path.join(COMPILED_FOLDER, 'ticket_details_{0}-noBOM.csv'.format(DATESTRING))
history_output_filename = os.path.join(COMPILED_FOLDER, 'ticket_history_{0}-noBOM.csv'.format(DATESTRING))

details = []
history = []
for details_csv_filename in details_csv_filenames:
    print("Reading in " + details_csv_filename)
    with open(details_csv_filename, 'rb') as f:
        details += list(csv.DictReader(f))
for history_csv_filename in history_csv_filenames:
    print("Reading in " + history_csv_filename)
    with open(history_csv_filename, 'rb') as f:
        history += list(csv.DictReader(f))

print("Writing out ticket_details to {0}".format(details_output_filename))
with open(details_output_filename, 'wb') as f:
    fieldnames = sorted(details[0].keys())
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(details)
print("Writing out ticket_history to {0}".format(history_output_filename))
with open(history_output_filename, 'wb') as f:
    fieldnames = sorted(history[0].keys())
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(history)

