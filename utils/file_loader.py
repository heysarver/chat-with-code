from langchain_community.document_loaders import TextLoader

def load_files(file_list):
    files = []
    for file in file_list:
        loader = TextLoader(file)
        files.extend(loader.load())
    return files
