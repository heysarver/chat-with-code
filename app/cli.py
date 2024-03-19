import click
from utils.embeddings import embeddings
from loaders.text_loader import load_text_files
from utils.text_processing import split_documents
from utils.vectorstores import create_deeplake, load_deeplake
from utils.chat import chat
from utils.chains import crc_from_llm

def register_cli(app):
    @app.cli.command()
    def load():
        src = app.config['REPO_URL']
        embs = embeddings()
        docs = load_text_files(src, delete_src_when_done=False)
        texts = split_documents(docs)
        db = create_deeplake(texts=texts, embeddings=embs, username=app.config['ACTIVELOOP_USERNAME'], dataset_name=app.config['VECTORDB_NAME'])
        return db
    
    @app.cli.command()
    @click.option('--questions', type=str)
    def query(questions):
        embs = embeddings()
        db = load_deeplake(username=app.config['ACTIVELOOP_USERNAME'], dataset_name=app.config['VECTORDB_NAME'], embeddings=embs)
        retriever = db.as_retriever()
        retriever.search_kwargs['distance_metric'] = 'cos'
        retriever.search_kwargs['fetch_k'] = 100
        retriever.search_kwargs['k'] = 10

        model_name = app.config['LLM_MODEL']
        llm_provider = app.config['LLM_PROVIDER']
        model = chat(temperature=0.2, provider=llm_provider, model_name=model_name)
        qa = crc_from_llm(model, retriever)

        questions = questions.split('|')

        chat_history = []

        for question in questions:
            result = qa({"question": question, "chat_history": chat_history})
            chat_history.append((question, result['answer']))
            print(f"**Question**: {question} \n")
            print(f"**Answer**: {result['answer']} \n\n\n\n")
