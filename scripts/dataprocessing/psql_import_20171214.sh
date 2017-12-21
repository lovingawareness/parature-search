#!/bin/bash -x
# This is where all data folders reside
ROOT_FOLDER=/data/Parature
# This is where the $HISTORICAL_FOLDER, unchanging data dumps exist for before the current year
HISTORICAL_FOLDER=$ROOT_FOLDER/historical
# This is where the data dumps exist for the current year, including the full customer export
CURRENT_FOLDER=$ROOT_FOLDER/current
# This is where the $HISTORICAL_FOLDER and current data dumps are combined into single CSV files
COMPILED_FOLDER=$ROOT_FOLDER/compiled
# This is the date string found in the current data dump
DATESTRING=20171214
# Insert these files into the PostgreSQL database, into the import schema
echo Inserting data files into the PostgreSQL database...
echo Processing customer data file.
./pgfutter --pass postgres --table customer csv $COMPILED_FOLDER/customer_$DATESTRING-noBOM-deduped-sanitized.csv
echo Processing ticket_details data file.
./pgfutter --pass postgres --table ticket_details csv $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-sanitized.csv
echo Processing ticket_history data file.
./pgfutter --pass postgres --table ticket_history csv $COMPILED_FOLDER/ticket_history_$DATESTRING-noBOM-sanitized.csv

