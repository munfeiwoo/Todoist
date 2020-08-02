from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def es_connect(hostname, port, username, password):
    es = Elasticsearch(hosts=[{'host': hostname, 'port': port}],
                       http_auth=(username, password))
    if es.ping():
        print('ES - Connected')
    else:
        print('ES - Failed to connect!')
    assert es.ping() is True
    return es
