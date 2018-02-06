from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()

class CustomerIndex(DocType):
    text = Text()

    class Meta:
        index = 'customer-index'

def bulk_indexing():
    print("Initiating CustomerIndex.")
    CustomerIndex.init()
    print("Inited CustomerIndex. Creating Elasticsearch instance.")
    es = Elasticsearch()
    print("Created Elasticsearch instance. Starting bulk index.")
    bulk(client=es, actions=(c.indexing() for c in models.Customer.objects.all().iterator()))
    print("Finished bulk index.")

def customer_search(partial_text):
    client = Elasticsearch()
    s = Search(using=client, index='customer-index').filter('wildcard', text=partial_text).scan()
    return s
