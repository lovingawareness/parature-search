#!/usr/bin/python
# dedupe_customer_csv.py
import sys
import unicodecsv as csv

with open(sys.argv[1], 'rb') as f:
    customers = list(csv.reader(f))

original_fieldnames, customers = customers[0], customers[1:]

dupes = set(list(original_fieldnames))
def indices(value, lst):
    """
    Finds the indices of all occurrences of value in lst.
    >>> indices(0, [0,1])
    [0]
    >>> indices(0, [0,1,0])
    [0,2]
    >>> indices(0, [1,2])
    []
    """
    _indices = []
    for i, v in enumerate(lst):
        if v == value:
            _indices.append(i)
    return _indices

# Let's create a dictionary of deduplicated field names and their corresponding source column index
source_index = {}
for dupe in dupes:
    unique_count = lambda i: len(set([c[i] for c in customers]))
    x = indices(dupe, original_fieldnames)
    y = map(unique_count, x)
    source_index[dupe], _ = zip(x, y)[y.index(max(y))]

for i, fieldname in enumerate(original_fieldnames):
    if fieldname not in dupes:
        source_index[fieldname] = i

rows = [{fieldname: customer[index] for fieldname, index in source_index.iteritems()} for customer in customers]

with open(sys.argv[2], 'wb') as f:
    dw = csv.DictWriter(f, fieldnames=sorted(source_index.keys()))
    dw.writeheader()
    dw.writerows(rows)
