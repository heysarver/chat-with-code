import os
from utils.git_utils import clone_repo, get_repo_name
from lib.embedding import embed_files, text_to_vector, load_model
from lib.elasticsearch import store_documents, delete_es_index, semantic_search, get_es_object
from transformers import AutoTokenizer, AutoModel
from elasticsearch import Elasticsearch

class App:
    def __init__(self, args):
        self.codebase_name = args.codebase_name
        self.file_extensions = args.file_extensions.split(',')
        self.source_dir = args.local_path if args.local_path else "data/source"
        self.github_repo = args.github_repo
        self.elasticsearch_index = args.elasticsearch_index
        self.elasticsearch_scheme = args.elasticsearch_scheme
        self.elasticsearch_host = args.elasticsearch_host
        self.elasticsearch_port = args.elasticsearch_port
        self.elasticsearch_verify_certs = args.elasticsearch_verify_certs
        self.elasticsearch_username = args.elasticsearch_username
        self.elasticsearch_password = args.elasticsearch_password
        self.elasticsearch_delete_index = args.elasticsearch_delete_index
        self.embedding_provider = args.embedding_provider
        self.embedding_model = args.embedding_model
        self.chunk_length = args.chunk_length
        self.chunk_overlap = args.chunk_overlap
        self.search_results = args.search_results
        self.search_match_percentage = args.search_match_percentage
        self.skip_embedding = args.skip_embedding
        
        self.documents = None

        if self.github_repo:
            clone_repo(self.github_repo, self.source_dir)
            self.codebase_name = self.codebase_name or get_repo_name(self.github_repo)

    def get_es_object(self):
        return(get_es_object(self))

    def file_list(self):
        files = []
        for dirpath, dirnames, filenames in os.walk(self.source_dir):
            for filename in filenames:
                if filename.endswith(tuple(self.file_extensions)):
                    files.append(os.path.join(dirpath, filename))
        return files
    
    def create_documents(self, provider, model):
        if not provider:
            provider = self.embedding_provider
        if not model:
            model = self.embedding_model

        print(f"Creating documents using {provider} and {model}")
        
        texts, embeddings, metadatas = embed_files(self.file_list(), provider, model, self.chunk_length, self.chunk_overlap)

        documents = []

        for i in range(len(texts)):
            metadata = metadatas[i]
            for key, value in metadata.items():
                if isinstance(value, str):
                    metadata[key] = value.replace(self.source_dir, self.codebase_name)
            
            document = {
                "text": texts[i],
                "embedding": embeddings[i],
                "metadata": metadatas[i]
            }
            documents.append(document)
        
        self.documents = documents

    def store_documents(self, index=None, recreate_index=None):
        if not index:
            index = self.elasticsearch_index
        if not recreate_index:
            recreate_index = self.elasticsearch_delete_index
        return store_documents(self, index, recreate_index)
    
    def delete_es_index(self, index=None):
        if not index:
            index = self.elasticsearch_index
        delete_es_index(self, index)

    def semantic_search(self, query, index=None, size=None):
        if not index:
            index = self.elasticsearch_index
        if not size:
            size = self.search_results
        
        return semantic_search(self, query, index, size)
