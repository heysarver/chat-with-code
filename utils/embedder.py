from langchain.text_splitter import CharacterTextSplitter
# from utils.file_loader import load_files
from langchain_community.document_loaders import TextLoader

def load_files(file_list):
    docs = []
    for file in file_list:
        loader = TextLoader(file)
        docs.extend(loader.load())
        print(f'Loaded {len(docs)} documents from {file}')  # Debug output
    return docs

def embed_files(file_list, provider, model):
    docs = load_files(file_list)
    print(f'Total documents to embed: {len(docs)}')  # Debug output
    # print(docs)
    chunks = split_docs(docs)

def split_docs(docs, chunk_size=1000, overlap=100):
    text_splitter = CharacterTextSplitter(chunk_size, overlap)
    chunked_documents = []
    for doc in docs:
        # print(doc.page_content)
        chunks = text_splitter.split_documents(doc)
        chunked_documents.extend(chunks)
    # print(f'Total chunks: {len(chunked_documents)}')  # Debug output
