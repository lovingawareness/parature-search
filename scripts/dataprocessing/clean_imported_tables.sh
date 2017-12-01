#!/bin/bash
sudo -u postgres psql -d postgres -a -f /data/Parature/clean_imported_tables.sql
