#!/bin/bash
PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d $DB_NAME -a -f ./clean_imported_tables.sql
