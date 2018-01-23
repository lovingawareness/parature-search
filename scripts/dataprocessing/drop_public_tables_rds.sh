#!/bin/bash -x
PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d $DB_NAME -a -f ./drop_public_tables.sql
