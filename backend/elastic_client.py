from elasticsearch import Elasticsearch

ES_HOST = "http://localhost:9200"
INDEX_NAME = "rvce"

def get_es_client():
    return Elasticsearch(ES_HOST)
