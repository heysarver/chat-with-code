from app.app import App
from elasticsearch import Elasticsearch
from pprint import pprint

import argparse
import os
from dotenv import load_dotenv

def parse_args():
    load_dotenv()

    GITHUB_REPO = os.getenv("GITHUB_REPO", "")
    LOCAL_PATH = os.getenv("LOCAL_PATH", "")
    FILE_EXTENSIONS = os.getenv("FILE_EXTENSIONS", ".py,.md")
    CODEBASE_NAME = os.getenv("CODEBASE_NAME", "local")
    ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", CODEBASE_NAME + "_vectors")
    ELASTICSEARCH_SCHEME = os.getenv("ELASTICSEARCH_SCHEME", "https")
    ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
    ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT", 9200)
    ELASTICSEARCH_VERIFY_CERTS = os.getenv("ELASTICSEARCH_VERIFY_CERTS", False)
    ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
    ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "password")
    ELASTICSEARCH_DELETE_INDEX = os.getenv("ELASTICSEARCH_DELETE_INDEX", True)
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "bigcode/starcoder2-3b")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    CHUNK_LENGTH = os.getenv("CHUNK_LENGTH", 1024)
    CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP", 128)
    SEARCH_RESULTS = os.getenv("SEARCH_RESULTS", 50)
    SEARCH_MATCH_PERCENTAGE = os.getenv("SEARCH_MATCH_PERCENTAGE", 0.8)
    SKIP_EMBEDDING = os.getenv("SKIP_EMBEDDING", False)
    SKEW_PHRASE = os.getenv("SKEW_PHRASE", None)
    SKEW_PHRASE_BOOST = os.getenv("SKEW_PHRASE_BOOST", 0.5)

    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument("--github-repo", type=str, default=GITHUB_REPO, help="GitHub repository URL")
    parser.add_argument("--local-path", type=str, default=LOCAL_PATH, help="Local path to clone the repository")  
    parser.add_argument("--file-extensions", type=str, default=FILE_EXTENSIONS, help="File extensions to embed, e.g. '.py,.md'")  
    parser.add_argument("--codebase-name", type=str, default=CODEBASE_NAME, help="Name of the codebase")
    parser.add_argument("--elasticsearch-index", type=str, default=ELASTICSEARCH_INDEX, help="Name of the elasticsearch index")
    parser.add_argument("--elasticsearch-scheme", type=str, default=ELASTICSEARCH_SCHEME, help="Scheme of the elasticsearch host")
    parser.add_argument("--elasticsearch-host", type=str, default=ELASTICSEARCH_HOST, help="Host of the elasticsearch")
    parser.add_argument("--elasticsearch-port", type=str, default=ELASTICSEARCH_PORT, help="Port of the elasticsearch")
    parser.add_argument("--elasticsearch-verify-certs", type=bool, default=ELASTICSEARCH_VERIFY_CERTS, help="Verify certificates of the elasticsearch")
    parser.add_argument("--elasticsearch-username", type=str, default=ELASTICSEARCH_USERNAME, help="Username of the elasticsearch")
    parser.add_argument("--elasticsearch-password", type=str, default=ELASTICSEARCH_PASSWORD, help="Password of the elasticsearch")
    parser.add_argument("--elasticsearch-delete-index", type=bool, default=ELASTICSEARCH_DELETE_INDEX, help="Delete the index before saving embeddings")
    parser.add_argument("--embedding-provider", type=str, default=EMBEDDING_PROVIDER, help="Provider for embedding")
    parser.add_argument("--embedding-model", type=str, default=EMBEDDING_MODEL, help="Model for embedding")
    parser.add_argument("--openai-api-key", type=str, default=OPENAI_API_KEY, help="OpenAI API key")
    parser.add_argument("--chunk-length", type=int, default=CHUNK_LENGTH, help="Length of the chunk")
    parser.add_argument("--chunk-overlap", type=int, default=CHUNK_OVERLAP, help="Overlap of the chunk")
    parser.add_argument("--search-results", type=int, default=SEARCH_RESULTS, help="Number of search results")
    parser.add_argument("--search-match-percentage", type=float, default=SEARCH_MATCH_PERCENTAGE, help="Match percentage for search")
    parser.add_argument("--skip-embedding", type=bool, default=SKIP_EMBEDDING, help="Skip embedding")
    parser.add_argument("--skew-phrase", type=str, default=SKEW_PHRASE, help="Skew phrase")
    parser.add_argument("--skew-phrase-boost", type=float, default=SKEW_PHRASE_BOOST, help="Skew phrase boost")

    args = parser.parse_args()
    if args.github_repo != "" and args.local_path != "":
        raise ValueError("Cannot specify both github-repo and local-path.  Please specify only one.")

    return args

def print_search_results(search_result):
    hits = search_result['hits']['hits']
    for i, hit in enumerate(hits, start=1):
        source = hit['_source']
        text = source['text']
        metadata = source['metadata']
        score = hit['_score']
        score = round((score / 2) * 100, 2)  # update score calculation
        print(f"Result {i}:")
        print(f"Score: {score}%")  # print score as a percentage
        print(f"Metadata: {metadata}")
        print("\n")

if __name__ == "__main__":
    args = parse_args()
    app = App(args)
    if not app.skip_embedding:
        app.create_documents(provider=args.embedding_provider, model=args.embedding_model)
        app.store_documents()
    search_result = app.search(query = "generate sample code for create_transaction")
    print_search_results(search_result)
