from elasticsearch import Elasticsearch
from common import Singleton


class ElasticSearch(object):

    __es_client = None

    def __init__(self):
        self.__es_client = Elasticsearch(hosts=['http://localhost:9200'])


if __name__ == '__main__':
    es = ElasticSearch()
    print(es)
