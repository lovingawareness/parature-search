FOLDER=compiled
DATESTRING=20171214
# Copy the customer file from the current folder to the compiled folder
cp current/customer_$DATESTRING.csv $FOLDER/
# Remove BOM
echo Removing BOM...
echo Processing customer data file.
tail -c +4 $FOLDER/customer_$DATESTRING.csv > $FOLDER/customer_$DATESTRING-noBOM.csv
echo Processing the historical ticket details files.
tail -c +4 historical/ticket_details_20121231-20000101.csv > historical/noBOM/ticket_details_20121231-20000101-noBOM.csv
tail -c +4 historical/ticket_details_20131231-20130101.csv > historical/noBOM/ticket_details_20131231-20130101-noBOM.csv
tail -c +4 historical/ticket_details_20141231-20140101.csv > historical/noBOM/ticket_details_20141231-20140101-noBOM.csv
tail -c +4 historical/ticket_details_20151231-20150101.csv > historical/noBOM/ticket_details_20151231-20150101-noBOM.csv
tail -c +4 historical/ticket_details_20161231-20160101.csv > historical/noBOM/ticket_details_20161231-20160101-noBOM.csv
echo Processing the historical ticket history files.
tail -c +4 historical/ticket_history_20111231-20000101.csv > historical/noBOM/ticket_history_20111231-20000101-noBOM.csv
tail -c +4 historical/ticket_history_20121231-20120101.csv > historical/noBOM/ticket_history_20121231-20120101-noBOM.csv
tail -c +4 historical/ticket_history_20131231-20130101.csv > historical/noBOM/ticket_history_20131231-20130101-noBOM.csv
tail -c +4 historical/ticket_history_20141231-20140101.csv > historical/noBOM/ticket_history_20141231-20140101-noBOM.csv
tail -c +4 historical/ticket_history_20151231-20150101.csv > historical/noBOM/ticket_history_20151231-20150101-noBOM.csv
tail -c +4 historical/ticket_history_20161231-20160101.csv > historical/noBOM/ticket_history_20161231-20160101-noBOM.csv
echo Processing the current ticket detail file.
tail -c +4 current/ticket_details_$DATESTRING-20170101.csv > current/noBOM/ticket_details_$DATESTRING-20170101-noBOM.csv
echo Processing the current ticket history file.
tail -c +4 current/ticket_history_$DATESTRING-20170101.csv > current/noBOM/ticket_history_$DATESTRING-20170101-noBOM.csv
echo Compile the historical and current ticket details and history files into single files each.
python compile_csvs_from_historical_and_current.py $DATESTRING
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

