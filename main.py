import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import DeepLake
from langchain_openai import OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings
from utils.git import clone_repo, get_repo_name

load_dotenv()

if os.environ.get("EMBEDDING_PROVIDER") == "voyageai":
    embeddings = VoyageAIEmbeddings(voyage_api_key=os.environ.get("VOYAGE_API_KEY"), model="voyage-2")
elif os.environ.get("EMBEDDING_PROVIDER") == "openai":
    embeddings = OpenAIEmbeddings(disallowed_special=())

repo_url = os.environ.get("GIT_REPO")
repo_name = get_repo_name(repo_url)

root_dir = f"./{repo_name}"

print(f"Cloning {repo_url}")
clone_repo(repo_url, repo_name)

docs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        try:
            loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
            docs.extend(loader.load_and_split())
        except Exception as e:
            pass

print(f"Loaded {len(docs)} files from {root_dir}")

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)

username = os.environ.get('ACTIVELOOP_USERNAME')
dataset_name = os.environ.get('VECTORDB_NAME')
dataset_path = f"hub://{username}/{dataset_name}"

try:
    db = DeepLake(dataset_path=dataset_path, embedding=embeddings, overwrite=True)
except Exception as e:
    print(f"Error: {e}")

db.add_documents(texts)

db = DeepLake(dataset_path=dataset_path, read_only=True, embedding=embeddings)

retriever = db.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['fetch_k'] = 100
retriever.search_kwargs['k'] = 10

model_name = os.environ.get("LLM_MODEL")
model = ChatAnthropic(temperature=0.2, model_name="claude-3-sonnet-20240229")
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

questions = ["How do I connect to a sandbox instance of the tastytrade api?",
             "How do I view the net liquidity history of an account?",
             "Generate a python script to get the net liquidity history of an account in the sandbox environment.",]

chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result['answer']))
    print(f"**Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n\n\n\n")
