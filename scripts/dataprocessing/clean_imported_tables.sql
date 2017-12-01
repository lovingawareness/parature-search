-- 
-- Create new tables in the public schema mimicking the structure of the tables in the import schema
--
create table public.customer (like import.customer including all);
create table public.ticket_details (like import.ticket_details including all);
create table public.ticket_history (like import.ticket_history including all);
-- 
-- Copy the data from the same-named tables in the import schema into the public schema
--
insert into public.customer select * from import.customer;
insert into public.ticket_details select * from import.ticket_details;
insert into public.ticket_history select * from import.ticket_history;
-- 
-- Convert the primary key fields in the customer and ticket_details tables to integers
--
ALTER TABLE public.customer ALTER COLUMN customerid TYPE integer USING (customerid::integer);
ALTER TABLE public.ticket_details ALTER COLUMN ticketid TYPE integer USING (ticketid::integer);
-- 
-- Add a primary key field to the customer table and copy values from the customerid column
-- 
ALTER TABLE public.customer ADD COLUMN id SERIAL;
UPDATE public.customer SET id = customerid;
-- 
-- Add a primary key field to the ticket_details table and copy values from the ticketid column
-- 
ALTER TABLE public.ticket_details ADD COLUMN id SERIAL;
UPDATE public.ticket_details SET id = ticketid;
-- 
-- Add a primary key field to the ticket_history table and let it auto-populate
-- 
ALTER TABLE public.ticket_history ADD COLUMN id SERIAL;
--
-- Convert the customerid column in ticket_details to an integer and make it a foreign key to the customer table
--
ALTER TABLE public.ticket_details ALTER COLUMN customerid TYPE integer USING (customerid::integer);
ALTER TABLE public.customer ADD CONSTRAINT fk_customer_customerid UNIQUE (customerid);
ALTER TABLE public.ticket_details
   ADD CONSTRAINT fk_links_ticket_details_customer
   FOREIGN KEY (customerid)
   REFERENCES public.customer(customerid);
--
-- Convert the ticket_id column in ticket_history to an integer and make it a foreign key to the ticket_details table
--
ALTER TABLE public.ticket_history ALTER COLUMN ticket_id TYPE integer USING (ticket_id::integer);
ALTER TABLE public.ticket_details ADD CONSTRAINT fk_ticket_details_ticketid UNIQUE (ticketid);
ALTER TABLE public.ticket_history
   ADD CONSTRAINT fk_links_ticket_history_ticket_details
   FOREIGN KEY (ticket_id)
   REFERENCES public.ticket_details(ticketid);
--
-- Convert the date strings into actual date field types
--
ALTER TABLE public.ticket_history ALTER COLUMN action_date TYPE timestamp USING to_timestamp(action_date, 'Mon DD YYYY HH:MIPM');
ALTER TABLE public.ticket_details ALTER COLUMN datecreated TYPE timestamp USING to_timestamp(datecreated, 'Mon DD YYYY HH:MIPM');
ALTER TABLE public.ticket_details ALTER COLUMN dateupdated TYPE timestamp USING to_timestamp(dateupdated, 'Mon DD YYYY HH:MIPM');
ALTER TABLE public.customer ALTER COLUMN date_created TYPE timestamp USING to_timestamp(date_created, 'Mon DD YYYY HH:MIPM');
ALTER TABLE public.customer ALTER COLUMN date_modified TYPE timestamp USING to_timestamp(date_modified, 'Mon DD YYYY HH:MIPM');

