from langchain_text_splitters import CharacterTextSplitter

def split_documents(docs):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)
