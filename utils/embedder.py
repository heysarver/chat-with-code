import os
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from utils.file_loader import load_files

def embed_files(file_list, provider, model):
    docs = load_files(file_list)
    chunks = split_docs(docs=docs)

    print(f"Embedding {len(chunks)} chunks")

    embeddings = []

def debug_overlap(text_docs, chunk_overlap):
    # Create directory if not exists
    if not os.path.exists('temp'):
        os.makedirs('temp')

    for i in range(1, len(text_docs)):
        # Open a new file for each overlap
        with open(f'temp/overlap_{i-1}_{i}.txt', 'w') as f:
            f.write("/* Overlap between chunk {i-1} and {i} */\n")
            f.write("/* End of chunk {i-1} */\n")
            f.write(f"{text_docs[i-1].page_content[-chunk_overlap:]}\n")  # Change here
            f.write("/* Start of chunk {i} */\n")
            f.write(f"{text_docs[i].page_content[:chunk_overlap]}\n")  # And here

def split_docs(docs, chunk_size=1000, chunk_overlap=100):
    # text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=[" ", ",", "\n"])
    document_chunks = []
 
    for doc in docs:
        content = doc.page_content
        metadata = doc.metadata

        text_docs = text_splitter.create_documents([content])
        print(f"Number of chunks: {len(text_docs)}")

        debug_overlap(text_docs, chunk_overlap)

        for tdoc in text_docs:
            # Add the metadata from the original document to each chunk
            chunk = {
                'text': tdoc,
                'metadata': metadata
            }
            document_chunks.append(chunk)

    return document_chunks
