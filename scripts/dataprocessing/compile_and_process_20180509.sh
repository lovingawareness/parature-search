#!/bin/bash -x
# http://www.faqs.org/docs/abs/HTML/options.html
# This is where all data folders reside
ROOT_FOLDER=/data/Parature
# This is where the $HISTORICAL_FOLDER, unchanging data dumps exist for before the current year
HISTORICAL_FOLDER=$ROOT_FOLDER/historical
# This is where the data dumps exist for the current year, including the full customer export
CURRENT_FOLDER=$ROOT_FOLDER/current
# This is where the $HISTORICAL_FOLDER and current data dumps are combined into single CSV files
COMPILED_FOLDER=$ROOT_FOLDER/compiled
# This is the date string found in the current data dump
DATESTRING=20180509
# Copy the customer file from the $CURRENT_FOLDER folder to the compiled folder
cp $CURRENT_FOLDER/customer_$DATESTRING.csv $COMPILED_FOLDER/
# Remove BOM
echo Removing BOM...
echo Processing customer data file.
tail -c +4 $COMPILED_FOLDER/customer_$DATESTRING.csv > $COMPILED_FOLDER/customer_$DATESTRING-noBOM.csv
echo Processing the $HISTORICAL_FOLDER ticket details files.
tail -c +4 $HISTORICAL_FOLDER/ticket_details_20111231-20070101.csv > $HISTORICAL_FOLDER/noBOM/ticket_details_20111231-20070101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_details_20121231-20120101.csv > $HISTORICAL_FOLDER/noBOM/ticket_details_20121231-20120101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_details_20131231-20130101.csv > $HISTORICAL_FOLDER/noBOM/ticket_details_20131231-20130101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_details_20141231-20140101.csv > $HISTORICAL_FOLDER/noBOM/ticket_details_20141231-20140101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_details_20151231-20150101.csv > $HISTORICAL_FOLDER/noBOM/ticket_details_20151231-20150101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_details_20161231-20160101.csv > $HISTORICAL_FOLDER/noBOM/ticket_details_20161231-20160101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_details_20171231-20170101.csv > $HISTORICAL_FOLDER/noBOM/ticket_details_20171231-20170101-noBOM.csv
echo Processing the $HISTORICAL_FOLDER ticket history files.
tail -c +4 $HISTORICAL_FOLDER/ticket_history_20111231-20070101.csv > $HISTORICAL_FOLDER/noBOM/ticket_history_20111231-20070101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_history_20121231-20120101.csv > $HISTORICAL_FOLDER/noBOM/ticket_history_20121231-20120101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_history_20131231-20130101.csv > $HISTORICAL_FOLDER/noBOM/ticket_history_20131231-20130101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_history_20141231-20140101.csv > $HISTORICAL_FOLDER/noBOM/ticket_history_20141231-20140101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_history_20151231-20150101.csv > $HISTORICAL_FOLDER/noBOM/ticket_history_20151231-20150101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_history_20161231-20160101.csv > $HISTORICAL_FOLDER/noBOM/ticket_history_20161231-20160101-noBOM.csv
tail -c +4 $HISTORICAL_FOLDER/ticket_history_20171231-20170101.csv > $HISTORICAL_FOLDER/noBOM/ticket_history_20171231-20170101-noBOM.csv
echo Processing the $CURRENT_FOLDER ticket detail file.
tail -c +4 $CURRENT_FOLDER/ticket_details_$DATESTRING-20180101.csv > $CURRENT_FOLDER/noBOM/ticket_details_$DATESTRING-20180101-noBOM.csv
echo Processing the $CURRENT_FOLDER ticket history file.
tail -c +4 $CURRENT_FOLDER/ticket_history_$DATESTRING-20180101.csv > $CURRENT_FOLDER/noBOM/ticket_history_$DATESTRING-20180101-noBOM.csv
echo Compile the $HISTORICAL_FOLDER and $CURRENT_FOLDER ticket details and history files into single files each.
python compile_csvs_from_historical_and_current.py $DATESTRING $HISTORICAL_FOLDER $CURRENT_FOLDER $COMPILED_FOLDER
# Dedupe the columns in the customer data file
echo Deduping columns in customer data file...
python dedupe_customer_csv.py $COMPILED_FOLDER/customer_$DATESTRING-noBOM.csv $COMPILED_FOLDER/customer_$DATESTRING-noBOM-deduped.csv
echo Here are the columns with numbers in ticket details:
csvcut -n $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM.csv
echo Removing RETIRED columns and "Maintenance/Task Type" column from ticket_details data file...
csvcut -c 1-8,10-16,79-107 $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM.csv > $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv
# Reset the blank customerIDs in ticket_details to an existing customerID
echo Resetting blank customerIDs in ticket_details to an existing customerID
python unblank_customer_ids_in_details.py $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-noblanks.csv
mv $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-noblanks.csv $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv
# Sanitize the field names in the data files
echo Sanitizing field names in the data files...
echo Processing customer data file.
python sanitize_csv_fieldnames.py $COMPILED_FOLDER/customer_$DATESTRING-noBOM-deduped.csv $COMPILED_FOLDER/customer_$DATESTRING-noBOM-deduped-sanitized.csv
echo Processing ticket_details data file.
python sanitize_csv_fieldnames.py $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed.csv $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-sanitized.csv
echo Processing ticket_history data file.
python sanitize_csv_fieldnames.py $COMPILED_FOLDER/ticket_history_$DATESTRING-noBOM.csv $COMPILED_FOLDER/ticket_history_$DATESTRING-noBOM-sanitized.csv
