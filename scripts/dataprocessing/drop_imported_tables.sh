#!/bin/bash
sudo -u postgres psql -d postgres -a -f /data/Parature/drop_imported_tables.sql
