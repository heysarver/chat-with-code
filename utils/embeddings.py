import os
from langchain_openai import OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings

def embeddings(provider: str = "voyageai", model: str = "voyage-2"):
    embeddings = None
    if provider == "voyageai":
        embeddings = VoyageAIEmbeddings(voyage_api_key=os.environ.get("VOYAGE_API_KEY"), model=model)
    elif provider == "openai":
        embeddings = OpenAIEmbeddings(disallowed_special=())
    else:
        raise ValueError(f"Unknown provider: {provider}")
    return embeddings
