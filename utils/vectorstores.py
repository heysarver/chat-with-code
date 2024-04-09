from langchain_community.vectorstores import DeepLake

def get_deeplake(username: str, dataset_name: str, embeddings: any, local: bool = True, read_only: bool = False):
    if local:
        scheme = "./deeplake/"
    else:
        scheme = "hub://"
    dataset_path = f"{scheme}{username}/{dataset_name}"
    db = DeepLake(dataset_path=dataset_path, read_only=read_only, embedding=embeddings)
    return db
