import logging
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler which logs even debug messages
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handler to logger
logger.addHandler(ch)

connections.create_connection()

class CustomerIndex(DocType):
    text = Text()

    class Meta:
        index = 'customer-index'


class TicketIndex(DocType):
    text = Text()

    class Meta:
        index = 'ticket-index'


def bulk_customers_indexing():
    logger.debug('Initiating CustomerIndex.')
    CustomerIndex.init()
    logger.debug("Inited CustomerIndex.")
    logger.debug("Creating Elasticsearch instance.")
    es = Elasticsearch()
    logger.debug("Created Elasticsearch instance.")
    logger.debug("Starting bulk index.")
    logger.debug("Bulk index: Customers")
    bulk(client=es, actions=(c.indexing() for c in models.Customer.objects.all().iterator()))
    logger.debug("Finished bulk index.")

def bulk_tickets_indexing():
    logger.debug("Initiating TicketIndex.")
    TicketIndex.init()
    logger.debug("Inited TicketIndex.")
    logger.debug("Creating Elasticsearch instance.")
    es = Elasticsearch()
    logger.debug("Created Elasticsearch instance.")
    logger.debug("Starting bulk index.")
    logger.debug("Bulk index: Tickets")
    bulk(client=es, actions=(t.indexing() for t in models.TicketDetails.objects.all().iterator()))
    logger.debug("Finished bulk index.")

def customer_search(query_string):
    client = Elasticsearch()
    if '*' in query_string or '?' in query_string:
        filter_type = 'wildcard'
        # Help people out with the fact that elasticsearch is case-sensitive but it stores text in lowercase in the index
        query_string = query_string.lower()
    else:
        # Don't mess with people's capitalization
        filter_type = 'match'

    s = Search(using=client, index='customer-index').filter(filter_type, text=query_string).scan()
    return s

def ticket_search(query_string, result_limit=None):
    client = Elasticsearch()
    if '*' in query_string or '?' in query_string:
        filter_type = 'wildcard'
        # Help people out with the fact that elasticsearch is case-sensitive but it stores text in lowercase in the index
        query_string = query_string.lower()
    else:
        # Don't mess with people's capitalization
        filter_type = 'match'

    s = Search(using=client, index='ticket-index').filter(filter_type, text=query_string)
    result = s.execute()
    results_count = result.hits.total
    if result_limit and results_count > result_limit:
        hits = list(s.scan())[:result_limit]
    else:
        hits = list(s.scan())
    ticket_ids = [int(hit.meta.id) for hit in hits]
    tickets = models.TicketDetails.objects.filter(id__in=ticket_ids).order_by('-id')
    return {'tickets': tickets, 'total_results': results_count}
