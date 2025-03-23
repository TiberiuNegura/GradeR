from flask import Flask
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config.from_object('app.config.Config')

    app.secret_key = os.getenv('SECRET_KEY')

    return app