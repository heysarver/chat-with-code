import os
from langchain_openai import OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings

def embeddings(provider: str, model: str):
    if provider == "voyageai":
        return embeddings_voyageai(model)
    elif provider == "openai":
        return embeddings_openai()
    else:
        raise ValueError(f"Unknown provider: {provider}")

def embeddings_openai():
    return OpenAIEmbeddings(disallowed_special=())

def embeddings_voyageai(model: str):
    return VoyageAIEmbeddings(voyage_api_key=os.environ.get("VOYAGE_API_KEY"), model=model)
