# Parature Data Processing

These scripts process the CSV data exports from Parature ticketing system, for customer and ticket data. The scripts first combine CSVs downloaded per year for ticket details and ticket history, remove vestigial columns from the ticket details, clean up formatting in the column names, remove the BOM bytes from the start of the files, and import the data into a PostgreSQL database.

## Preparing the PostgreSQL Database

### Drop the existing tables and relations

1. Drop the tables from the `import` schema: `./drop_imported_tables.sh`
2. Drop the tables from the `public` schema: `./drop_public_tables.sh`

## Process the CSV data

`./compile_and_process_20171214.sh`

# Import the processed CSV data to the PostgreSQL Database

`./psql_import_20171214.sh`

## PostgreSQL Database work - Copy to public schema, change data types, create relations

'./clean_imported_tables.sh`
