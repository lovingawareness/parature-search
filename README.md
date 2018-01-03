# parature-search
Historical Parature ticket search based on Django and PostgreSQL.

## Extract/Transform/Load Process

### Getting Data from Parature

First step is to actually get the data from Parature. 

From Internet Explorer (Parature being a product in the Microsoft world, it was designed for use with IE), download Parature ticket details and history year by year, and all of 2017 up to now. Put years prior to 2017 into folder `historical` and 2017 into `current`. Download the customer data to `current` as well. The file names should look like this:

Historical Files:

```
├── historical
│   ├── ticket_details_20121231-20000101.csv
│   ├── ticket_details_20131231-20130101.csv
│   ├── ticket_details_20141231-20140101.csv
│   ├── ticket_details_20151231-20150101.csv
│   ├── ticket_details_20161231-20160101.csv
│   ├── ticket_history_20111231-20000101.csv
│   ├── ticket_history_20121231-20120101.csv
│   ├── ticket_history_20131231-20130101.csv
│   ├── ticket_history_20141231-20140101.csv
│   ├── ticket_history_20151231-20150101.csv
│   └── ticket_history_20161231-20160101.csv
```

Current Files: 

```
├── current
│   ├── customer_20171214.csv
│   ├── ticket_details_20171214-20170101.csv
│   └── ticket_history_20171214-20170101.csv
```

### Processing Data from Parature

There's a great deal of cleanup we need to do, which is all wrapped up in this shell script [scripts/compile_and_process_20171214.sh](scripts/compile_and_process_20171214.sh), which relies on a few Python scripts as well. The output of this script are single files in the `compiled` folder:

```
compiled
├── customer_20171214-noBOM-deduped-sanitized.csv
├── ticket_details_20171214-noBOM-trimmed-sanitized.csv
└── ticket_history_20171214-noBOM-sanitized.csv
```

### Loading Data into PostgreSQL Database

These scripts all interact with a PostgreSQL database using the `psql` command. To use these, first set the following environment variables for the location of the PostgreSQL database and the login information:

```
export DB_NAME=
export DB_USER=
export DB_PASS=
export DB_HOST=
```

For example, if you have a local instance of PostgreSQL set up with very basic authentication, you might set:

```
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASS=postgres
export DB_HOST=localhost
```

Using an Amazon Web Services RDS database instance, you might have something more like:

```
export DB_NAME=parature
export DB_USER=paraturedb
export DB_PASS=5016,perfect,chair,hawaii,FISH,oslo,PERU,5812::::::::::::::::::
export DB_HOST=paratureticketsearch.c26bapazda4l.us-west-2.rds.amazonaws.com
```

#### Drop Existing Tables

If there is any table in the PostgreSQL database already, then the tables should be dropped. In this import process, they appear first in the `import` schema ("schema" is a PostgreSQL thing) and then re-processed for use by Django in the `public` schema. The following two SQL scripts will drop the tables in those schemas:

1. [scripts/drop_imported_tables.sql](scripts/drop_imported_tables.sql)
2. [scripts/drop_public_tables.sql](scripts/drop_public_tables.sql)

You can then use the following shell scripts to run those SQL scripts on the database, to drop the tables:

1. [scripts/drop_imported_tables_rds.sh](scripts/drop_imported_tables_rds.sh)
2. [scripts/drop_public_tables_rds.sh](scripts/drop_public_tables_rds.sh)

#### Load Data into PostgreSQL

TODO
Run [scripts/psql_import_rds_20171214.sh](scripts/psql_import_rds_20171214.sh).

#### Clean Up Data in PostgreSQL

There's a bit of cleanup we need to do in PostgreSQL, as the data is loaded all as pure text fields and they're in the `import` schema which is invisible to Django. We need to:

1. Create new tables in the `public` schema and copy over the data from the same tables in the `import` schema.
2. Convert the existing primary key fields in the `customer` and `ticket_details` tables from text to integer.
3. Create new columns in the `customer` and `ticket_details` tables that are actually recognized as the primary key by PostgreSQL, and follow the naming convention expected by Django, and copy the values from the existing values per row that can act as PK.
4. Create a new column in the `ticket_history` table that acts as primary key and let it auto-populate by PostgreSQL.
5. Create foreign key relations between `customer` and `ticket_details` tables, and between `ticket_details` and `ticket_history`.
6. Convert the columns in `ticket_details`, `ticket_history`, and `customer` with dates in them from text formats to timestamp formats recognized by PostgreSQL as representing date and time.

This is accomplished with the SQL script [scripts/clean_imported_tables.sql](scripts/clean_imported_tables.sql).

You can apply this SQL script to the server with [scripts/clean_imported_tables_rds.sh](scripts/clean_imported_tables_rds.sh).

