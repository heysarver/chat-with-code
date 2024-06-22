import click
from utils.embeddings import embeddings
from loaders.text_loader import load_text_files
from utils.text_processing import split_documents
from utils.vectorstores import get_deeplake
from utils.chat import chat
from utils.chains import crc_from_llm

def register_cli(app):
    @app.cli.command("load")
    @click.option('--repo_url', default=None, help='Override REPO_URL environment variable')
    def load(repo_url):
        if repo_url is not None:
            app.config['REPO_URL'] = repo_url
        src = app.config['REPO_URL']
        embs = embeddings(provider=app.config['EMBEDDING_PROVIDER'], model=app.config['EMBEDDING_MODEL'])
        docs = load_text_files(src, category="default") # category to be used in the future
        texts = split_documents(docs)
        db = get_deeplake(username=app.config['ACTIVELOOP_USERNAME'], dataset_name=app.config['VECTORDB_NAME'], embeddings=embs, local=True)
        db.add_documents(texts)
        return db
    
    @app.cli.command("query")
    @click.option('--questions', type=str)
    def query(questions):
        embs = embeddings(provider=app.config['EMBEDDING_PROVIDER'], model=app.config['EMBEDDING_MODEL'])
        db = get_deeplake(username=app.config['ACTIVELOOP_USERNAME'], dataset_name=app.config['VECTORDB_NAME'], embeddings=embs)
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
            print(f"**Question**:\n{question}\n")
            print(f"**Answer**:\n\n{result['answer']}\n\n")
