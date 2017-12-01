#!/usr/bin/python
# sanitize_csv_fieldnames.py
import sys
import unicodecsv as csv

replacements = (
    (' (PMA)',''),
    ('?',''),
    ('/',' or '),
    (' (NEW SC Other Field)',''),
    ('(confirm)', 'confirm'),
    ('[',''),
    (']',''),
    ('&amp;','and'),
    (' ','_'))


input_csv_filename = sys.argv[1]
output_csv_filename = sys.argv[2]
f_input = open(input_csv_filename, 'rb')
f_output = open(output_csv_filename, 'wb')
csv_reader = csv.reader(f_input)
csv_writer = csv.writer(f_output)
# Get just the first row for the fieldnames
fieldnames = csv_reader.next()
# Go through every field name, check for and do all the replacements we have set, and
# print out the replacement if it happens.
for i, fieldname in enumerate(fieldnames):
    original = fieldname
    changed = False
    for pattern, replacement in replacements:
        if pattern in fieldname:
            fieldname = fieldname.replace(pattern, replacement)
            changed = True
    if changed:
        print '"{0}" was changed to "{1}"'.format(original, fieldname)
    fieldnames[i] = fieldname
# Write these new rows to the output CSV
csv_writer.writerow(fieldnames)
# Write the rest of the rows
for row in csv_reader:
    csv_writer.writerow(row)

f_input.close()
f_output.close()
