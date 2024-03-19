import os
from dotenv import load_dotenv
from flask import Blueprint, Flask
from .api import api_blueprint
from .cli import register_cli

root_blueprint = Blueprint('root', __name__)
from . import routes

def load_config(app):
    config_vars = [
        ('EMBEDDING_PROVIDER', 'openai'),
        ('EMBEDDING_MODEL', 'voyage-2'),
        ('LLM_PROVIDER', 'openai'),
        ('LLM_MODEL', 'claude-3-sonnet-20240229'),
        ('ANTHROPIC_API_KEY', None),
        ('VOYAGE_API_KEY', None),
        ('OPENAI_API_KEY', ''),
        ('ACTIVELOOP_TOKEN', 'jwt'),
        ('ACTIVELOOP_USERNAME', 'username'),
        ('VECTORDB_NAME', 'chat-with-files'),
        ('VECTORDB_USERNAME', 'username'),
        ('VECTORDB_PASSWORD', ''),
        ('VECTORDB_HOST', ''),
        ('VECTORDB_PORT', ''),
        ('VECTORDB_PROVIDER', 'activeloop'),
        ('REPO_URL', 'https://github.com/username/repo'),
    ]

    for var, default in config_vars:
        app.config[var] = os.getenv(var, default)

def create_app():
    app = Flask(__name__)
    load_dotenv()
    load_config(app)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(root_blueprint)
    register_cli(app)
    return app
