#!/usr/bin/python
import unicodecsv as csv
import sys

input_csv_filename = sys.argv[1]
output_csv_filename = sys.argv[2]

with open(input_csv_filename, 'rb') as f:
    details = list(csv.DictReader(f))

for i, detail in enumerate(details):
    if detail[u'customerID'] == '':
        # Let's set these to the first customerID in the database, which corresponds to 
        # to the customer "AC Staff" with e-mail "paratureuser+acstaff@gmail.com"
        details[i][u'customerID'] = u'10010'


with open(output_csv_filename, 'wb') as f:
    fieldnames = sorted(details[0].keys())
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(details)
