FOLDER=compiled
DATESTRING=20171121
# Remove BOM
echo Removing BOM...
echo Processing customer data file.
tail -c +4 $FOLDER/customer_$DATESTRING.csv > $FOLDER/customer_$DATESTRING-noBOM.csv
# Dedupe the columns in the customer data file
echo Deduping columns in customer data file...
python dedupe_customer_csv.py $FOLDER/customer_$DATESTRING-noBOM.csv $FOLDER/customer_$DATESTRING-noBOM-deduped.csv
# Remove the RETIRED columns from ticket_details data file
echo Removing RETIRED columns from ticket_details data file...
csvcut -c 1-15,78-105 $FOLDER/ticket_details_$DATESTRING-noBOM.csv > $FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv
# Reset the blank customerIDs in ticket_details to an existing customerID
python unblank_customer_ids_in_details.py $FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv $FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-noblanks.csv
mv $FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-noblanks.csv $FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv
# Sanitize the field names in the data files
echo Sanitizing field names in the data files...
echo Processing customer data file.
python sanitize_csv_fieldnames.py $FOLDER/customer_$DATESTRING-noBOM-deduped.csv $FOLDER/customer_$DATESTRING-noBOM-deduped-sanitized.csv
echo Processing ticket_details data file.
python sanitize_csv_fieldnames.py $FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv $FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-sanitized.csv
echo Processing ticket_history data file.
python sanitize_csv_fieldnames.py $FOLDER/ticket_history_$DATESTRING-noBOM.csv $FOLDER/ticket_history_$DATESTRING-noBOM-sanitized.csv
# Insert these files into the PostgreSQL database, into the import schema
echo Inserting data files into the PostgreSQL database...
echo Processing customer data file.
./pgfutter --pass postgres --table customer csv ./$FOLDER/customer_$DATESTRING-noBOM-deduped-sanitized.csv
echo Processing ticket_details data file.
./pgfutter --pass postgres --table ticket_details csv ./$FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-sanitized.csv
echo Processing ticket_history data file.
./pgfutter --pass postgres --table ticket_history csv $FOLDER/ticket_history_$DATESTRING-noBOM-sanitized.csv

