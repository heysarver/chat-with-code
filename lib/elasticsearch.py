from elasticsearch import Elasticsearch
from lib.embedding import text_to_vector, load_model

def store_documents(app, index=None, recreate_index=False):
    if not index:
        index = app.elasticsearch_index

    es = get_es_object(app)

    if recreate_index:
        delete_es_index(app, index)

    for document in app.search_results:
        es.index(index=index, body=document)

def delete_es_index(app, index=None):
    if not index:
        index = app.elasticsearch_index
    es = get_es_object(app)

    if es.indices.exists(index=index):
        es.indices.delete(index=index)
    else:
        print(f"Index {index} does not exist.")

def semantic_search(app, query, index=None, size=10, skew_phrase=None, skew_phrase_boost=0, skew_phrase_field="text"):
    if not index:
        index = app.elasticsearch_index
    
    tokenizer, model = load_model(app.embedding_provider, app.embedding_model)
    query_vector = text_to_vector(query, tokenizer, model)
    es = get_es_object(app)

    search_query = {
        "function_score": {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "boost_mode": "replace"
        }
    }

    if skew_phrase and skew_phrase.strip():
        search_query["function_score"]["functions"] = [
            {
                "filter": {"match": {skew_phrase_field: skew_phrase}},
                "weight": skew_phrase_boost
            }
        ]
    
    response = es.search(
        index=index,
        body={
            "size": size,
            "query": search_query,
            "_source": ["text", "metadata"]  # fields to return
        }
    )

    return response

def get_es_object(app):
    es = Elasticsearch(
        hosts=[{
            "host": app.elasticsearch_host, 
            "port": app.elasticsearch_port, 
            "scheme": app.elasticsearch_scheme
        }],
        verify_certs=app.elasticsearch_verify_certs,
        ssl_show_warn=app.elasticsearch_verify_certs,
        http_auth=(app.elasticsearch_username, app.elasticsearch_password)
    )
    return es
