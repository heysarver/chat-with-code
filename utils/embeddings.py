import os
from langchain_openai import OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings

if os.environ.get("EMBEDDING_PROVIDER") == "voyageai":
    embeddings = VoyageAIEmbeddings(voyage_api_key=os.environ.get("VOYAGE_API_KEY"), model="voyage-2")
elif os.environ.get("EMBEDDING_PROVIDER") == "openai":
    embeddings = OpenAIEmbeddings(disallowed_special=())
