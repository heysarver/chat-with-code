from langchain.text_splitter import CharacterTextSplitter
from utils.file_loader import load_files

def embed_files(file_list, provider, model):
    docs = load_files(file_list)
    print(f'Total documents to embed: {len(docs)}')
    chunks = split_docs(docs=docs)
    print(f'Total chunks to embed: {len(chunks)}')

def split_docs(docs, chunk_size=1000, chunk_overlap=100):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = []

    for doc in docs:
        content = doc.page_content
        text = text_splitter.create_documents([content])
        texts.extend(text)
    
    return texts
