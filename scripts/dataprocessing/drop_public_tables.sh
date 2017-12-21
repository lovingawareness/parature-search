#!/bin/bash
sudo -u postgres psql -d postgres -a -f ./drop_public_tables.sql
