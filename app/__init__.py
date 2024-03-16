from flask import Flask
from .api import api_blueprint
from .cli import register_cli

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    register_cli(app)
    return app
