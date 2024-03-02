from langchain.text_splitter import CharacterTextSplitter
from utils.file_loader import load_files

def embed_files(file_list, provider, model):
    docs = load_files(file_list)
    print(f'Total documents to embed: {len(docs)}')  # Debug output
    print(type(docs))
    print(type(docs[0]))
    chunks = split_docs(docs)

def split_docs(docs, chunk_size=1000, overlap=100):
    text_splitter = CharacterTextSplitter(chunk_size, overlap)
    #chunked_documents = []

    chunks = text_splitter.split_documents(docs)
    #chunked_documents.extend(chunks)
    # print(f'Total chunks: {len(chunked_documents)}')  # Debug output
