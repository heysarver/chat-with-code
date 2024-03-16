from langchain.text_splitter import CharacterTextSplitter

def split_documents(docs):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(docs)
