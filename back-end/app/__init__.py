from flask import Flask
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config.from_object('app.config.Config')

    app.secret_key = os.getenv('SECRET_KEY')

    from app.routes.web_routes import web_bp
    app.register_blueprint(web_bp)

    from app.api import api_bp
    app.register_blueprint(api_bp)

    return app