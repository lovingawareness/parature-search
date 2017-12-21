#!/bin/bash
sudo -u postgres psql -d postgres -a -f ./drop_imported_tables.sql
