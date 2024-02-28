import argparse
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
from elasticsearch import Elasticsearch
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PythonLoader, UnstructuredMarkdownLoader

def parse_args():
    load_dotenv()

    GITHUB_REPO = os.getenv("GITHUB_REPO", "")
    FILE_EXTENSIONS = os.getenv("FILE_EXTENSION", ".py,.md")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-davinci-002")
    ELASTICSEARCH_SCHEME = os.getenv("ELASTICSEARCH_SCHEME", "https")
    ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
    ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT", 9200)
    ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "code_embeddings")

    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument("--github-repo", type=str, default=GITHUB_REPO, help="GitHub repository URL")
    parser.add_argument("--file-extensions", type=str, default=FILE_EXTENSIONS, help="File extensions to embed, e.g. '.py,.md'")
    parser.add_argument("--openai-api-key", type=str, default=OPENAI_API_KEY, help="OpenAI API Key")
    parser.add_argument("--openai-embedding-model", type=str, default=OPENAI_EMBEDDING_MODEL, help="OpenAI text embedding model")
    parser.add_argument("--elasticsearch-scheme", type=str, default=ELASTICSEARCH_SCHEME, help="Elasticsearch scheme")
    parser.add_argument("--elasticsearch-host", type=str, default=ELASTICSEARCH_HOST, help="Elasticsearch host")
    parser.add_argument("--elasticsearch-port", type=int, default=ELASTICSEARCH_PORT, help="Elasticsearch port")
    parser.add_argument("--elasticsearch-index", type=str, default=ELASTICSEARCH_INDEX, help="Elasticsearch index")

    return parser.parse_args()

def clone_repo(github_repo):
    repo_name = github_repo.split("/")[-1].replace(".git", "")
    repo_path = f"repos/{repo_name}"

    if not os.path.exists("repos"):
        os.makedirs("repos")

    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", github_repo, repo_path], check=True)
    else:
        print(f"Repository {repo_name} already exists. Skipping clone.")
    
    return repo_name

def list_embed_files(repo_name, file_extensions):
    embed_files = []
    file_extensions = file_extensions.split(',')
    for root, dirs, files in os.walk(f"repos/{repo_name}"):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                embed_files.append(os.path.join(root, file))
    return embed_files

def embed_and_store_files(files):
    documents = []
    for file in files:
        if file.endswith('.py'):
            loader = PythonLoader(file)
        elif file.endswith('.md'):
            loader = UnstructuredMarkdownLoader(file)
        else:
            continue
        documents.append(loader.load())
    
    



if __name__ == "__main__":
    args = parse_args()

    repo_name = clone_repo(args.github_repo)
    embed_files_list = list_embed_files(repo_name, args.file_extensions)

    es = Elasticsearch(hosts=[{'host': args.elasticsearch_host, 'port': args.elasticsearch_port, 'scheme': args.elasticsearch_scheme}])
    embed_and_store_files(files=embed_files_list, elasticsearch=es, elasticsearch_index=args.elasticsearch_index)
