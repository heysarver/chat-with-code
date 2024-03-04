from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_files(file_list):
    files = []
    for file in file_list:
        loader = TextLoader(file)
        files.extend(loader.load())
    return files

def split_docs(docs, chunk_size=1024, chunk_overlap=128):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=[" ", ",", "\n"])
    chunks = []

    print(f"Splitting {len(docs)} documents")
 
    for doc in docs:
        content = doc.page_content
        metadata = doc.metadata

        text_docs = text_splitter.create_documents([content])
        # print(f"Number of chunks: {len(text_docs)} for {metadata['source']}")

        for tdoc in text_docs:
            # Add the metadata from the original document to each chunk
            chunk = {
                'text': tdoc.page_content,
                'metadata': metadata
            }
            chunks.append(chunk)

    return chunks

def load_model(provider, model):
    if provider == "huggingface":
        tokenizer = AutoTokenizer.from_pretrained(model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        try:
            model = AutoModel.from_pretrained(model).to(device)
        except torch.cuda.OutOfMemoryError:
            print("Failed to load model with default data type. Retrying with bfloat16...")
            try:
                model = AutoModel.from_pretrained(model, torch_dtype=torch.bfloat16).to(device)
            except torch.cuda.OutOfMemoryError:
                print("Failed to load model with bfloat16. Retrying with int8...")
                try:
                    quantization_config = BitsAndBytesConfig(load_in_8bit=True)
                    model = AutoModel.from_pretrained(model, quantization_config=quantization_config)
                except torch.cuda.OutOfMemoryError:
                    print("Failed to load model with bfloat16. Retrying with int8...")
                    try:
                        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
                        model = AutoModel.from_pretrained(model, quantization_config=quantization_config)
                    except torch.cuda.OutOfMemoryError:
                        raise ValueError("Failed to load model with int4.  Out of memory.")
        return tokenizer, model
    elif provider == "openai":
        raise NotImplementedError("OpenAI embeddings extraction not implemented.")
    else:
        raise ValueError(f"Unknown provider: {provider}")

def text_to_vector(text, tokenizer, model):
    print(f"Embedding text of length {len(text)}")

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=1024)
    inputs = {name: tensor.to(device) for name, tensor in inputs.items()}
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().cpu().numpy()

def embed_files(file_list, provider, model_name, chunk_length=1024, chunk_overlap=128):
    docs = load_files(file_list)
    chunks = split_docs(docs=docs, chunk_size=chunk_length, chunk_overlap=chunk_overlap)

    print(f"Embedding {len(chunks)} chunks")

    if provider == "huggingface":
        texts = []
        embeddings = []
        metadatas = []
        tokenizer, model = load_model(provider, model_name)
        for chunk in chunks:
            text = chunk['text']
            metadata = chunk['metadata']
            metadatas.append(metadata)
            texts.append(text)
            embedding = text_to_vector(text, tokenizer, model)
            embeddings.append(embedding)

        return texts, embeddings, metadatas
    elif provider == "openai":
        raise NotImplementedError("OpenAI embeddings extraction not implemented.")
    else:
        raise ValueError(f"Unknown provider: {provider}")
