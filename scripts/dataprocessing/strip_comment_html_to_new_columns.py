#!/usr/bin/python
from collections import OrderedDict
import csv
import sys
import unicodedata
from htmllaundry import strip_markup
from tqdm import tqdm

replacements = OrderedDict([
    ('&amp;', '&'),
    ('&lt;', '<'),
    ('&gt;', '>'),
    ('&quot;', '"'),
    ('""', '"'),
    ('\n', ' '),
    ])

def clean_text(text):
    new_text = text
    new_text = new_text.decode('utf8')
    for k,v in replacements.items():
        new_text = new_text.replace(k, v)
    new_text = strip_markup(new_text)
    return unicodedata.normalize('NFKD', new_text).encode('ascii', 'ignore')


with open(sys.argv[1], 'rb') as f_input:
    with open(sys.argv[2], 'wb') as f_output:
        csv_reader = csv.DictReader(f_input)
        # Is this a ticket details or ticket history file? Check based on presence of key fields
        fieldnames = csv_reader.fieldnames
        if 'Details' in fieldnames:
            # Ticket Details
            cleaning_fields = {'Details': 'Details_nohtml', 'Solution': 'Solution_nohtml'}
        elif 'Comments' in fieldnames:
            # Ticket History
            cleaning_fields = {'Comments': 'Comments_nohtml'}
        else:
            # Not something we recognize, let's abort
            print("This is not a ticket details or ticket history CSV file.")
            sys.exit(1)
        # Built the fieldnames that will appear in the output file
        new_fieldnames = fieldnames + cleaning_fields.values()
        csv_writer = csv.DictWriter(f_output, fieldnames=new_fieldnames)
        csv_writer.writeheader()
        for row in tqdm(csv_reader):
            for original_field, new_field in cleaning_fields.items():
                row[new_field] = clean_text(row[original_field])
            csv_writer.writerow(row)
