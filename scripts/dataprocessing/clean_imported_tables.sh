#!/bin/bash
sudo -u postgres psql -d postgres -a -f ./clean_imported_tables.sql
