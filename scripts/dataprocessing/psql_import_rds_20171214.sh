#!/bin/bash -x
# This is where all data folders reside
ROOT_FOLDER=/data/Parature
# This is where the $HISTORICAL_FOLDER and current data dumps are combined into single CSV files
COMPILED_FOLDER=$ROOT_FOLDER/compiled
# This is the date string found in the current data dump
DATESTRING=20171214
# Insert these files into the PostgreSQL database, into the import schema
echo Inserting data files into the PostgreSQL database...
echo Make sure that the database host, username, and password are set with environment variables DB_HOST, DB_NAME, DB_USER, and DB_PASS.
echo Hostname: $DB_HOST
echo Database: $DB_NAME
echo Username: $DB_USER
echo Password: $DB_PASS
echo Processing customer data file.
./pgfutter --host $DB_HOST --dbname $DB_NAME --username $DB_USER --pass $DB_PASS --table customer csv $COMPILED_FOLDER/customer_$DATESTRING-noBOM-deduped-sanitized.csv
echo Processing ticket_details data file.
./pgfutter --host $DB_HOST --dbname $DB_NAME --username $DB_USER --pass $DB_PASS --table ticket_details csv $COMPILED_FOLDER/ticket_details_$DATESTRING-noBOM-trimmed-sanitized.csv
echo Processing ticket_history data file.
./pgfutter --host $DB_HOST --dbname $DB_NAME --username $DB_USER --pass $DB_PASS --table ticket_history csv $COMPILED_FOLDER/ticket_history_$DATESTRING-noBOM-sanitized.csv

