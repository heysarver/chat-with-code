import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import DeepLake

load_dotenv()







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
