from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def es_connect(hostname, port, username, password):
    es = Elasticsearch(hosts=[{'host': hostname, 'port': port}],
                       http_auth=(username, password))
    if es.ping():
        print('Connected')
    else:
        print('Failed to connect!')
    assert es.ping() is True
    return es


def es_search(es):
    return Search(using=es)
