import os
import dotenv
from elasticsearch import Elasticsearch

def connect_to_elasticsearch():
    es = Elasticsearch(
        [{
            "host": os.environ.get("ELASTICSEARCH_HOST", "localhost"),
            "port": os.environ.get("ELASTICSEARCH_PORT", 9200),
        }]
    )
    return es


def get_es_index_name():
    return os.environ.get("ELASTICSEARCH_INDEX_NAME", "test")


def get_es_index_type():
    return os.environ.get("ELASTICSEARCH_INDEX_TYPE", "test")


def get_es_index_settings():
    return {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            }
        }
    }


def get_es_index_mappings():
    return {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "age": {"type": "integer"},
                "date": {"type": "date"},
            }
        }
    }


def create_es_index(es, index_name, doc_type, settings, mappings):
    if not es.indices.exists(index=get_es_index_name(index_name)):
      es.indices.create(
          index=get_es_index_name(index_name),
          body=get_es_index_settings(settings),
          ignore=400,
      )
      es.indices.put_mapping(
          index=get_es_index_name(index_name),
          doc_type=get_es_index_type(doc_type),
          body=get_es_index_mappings(mappings),
      )

def delete_es_index(es, index_name):
    if es.indices.exists(index=get_es_index_name(index_name)):
        es.indices.delete(index=get_es_index_name(index_name), ignore=[400, 404])


if __name__ == "__main__":
    es = connect_to_elasticsearch()
    index_name = get_es_index_name()
    index_type = get_es_index_type()
    index_settings = get_es_index_settings()
    index_mappings = get_es_index_mappings()
    create_es_index(es, index_name, index_type, index_settings, index_mappings)
