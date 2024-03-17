import os
from dotenv import load_dotenv
from flask import Flask
from .api import api_blueprint
from .cli import register_cli

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['EMBEDDING_PROVIDER'] = os.getenv('EMBEDDING_PROVIDER', 'openai')
    app.config['EMBEDDING_MODEL'] = os.getenv('EMBEDDING_MODEL', 'voyage-2')
    app.config['LLM_PROVIDER'] = os.getenv('LLM_PROVIDER', 'openai')
    app.config['LLM_MODEL'] = os.getenv('LLM_MODEL', 'claude-3-sonnet-20240229')
    app.config['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')
    app.config['VOYAGE_API_KEY'] = os.getenv('VOYAGE_API_KEY')
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
    app.config['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN', 'jwt')
    app.config['ACTIVELOOP_USERNAME'] = os.getenv('ACTIVELOOP_USERNAME', 'username')
    app.config['VECTORDB_NAME'] = os.getenv('VECTORDB_NAME', 'chat-with-files')
    app.config['VECTORDB_USERNAME'] = os.getenv('VECTORDB_USERNAME', 'username')
    app.config['VECTORDB_PASSWORD'] = os.getenv('VECTORDB_PASSWORD', '')
    app.config['VECTORDB_HOST'] = os.getenv('VECTORDB_HOST', '')
    app.config['VECTORDB_PORT'] = os.getenv('VECTORDB_PORT', '')
    app.config['VECTORDB_PROVIDER'] = os.getenv('VECTORDB_PROVIDER', 'activeloop')
    app.config['REPO_URL'] = os.getenv('REPO_URL', 'https://github.com/username/repo')
    app.register_blueprint(api_blueprint)
    register_cli(app)
    return app
