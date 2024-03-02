from langchain_community.document_loaders import TextLoader

def load_files(file_list):
    docs = []
    for file in file_list:
        loader = TextLoader(file)
        docs.extend(loader.load())
    return docs
