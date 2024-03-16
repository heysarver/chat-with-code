import os
from langchain_community.vectorstores import DeepLake

def create_deeplake(texts: any, username: str, dataset_name: str, embeddings: any):
    dataset_path = f"hub://{username}/{dataset_name}"

    db = DeepLake(dataset_path=dataset_path, embedding=embeddings, overwrite=True)

    for text in texts:
        print(f"Adding document: {text}\n\n\n\n")

    db.add_documents(texts)

    return db

def load_deeplake(username: str, dataset_name: str, embeddings: any, read_only: bool = True):
    dataset_path = f"hub://{username}/{dataset_name}"

    db = DeepLake(dataset_path=dataset_path, read_only=True, embedding=embeddings)

    return db
