#!/bin/bash
sudo -u postgres psql -d postgres -a -f /data/Parature/drop_public_tables.sql
