import os

from dotenv import load_dotenv
from flask import Flask


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_FILE = os.path.join(ROOT_DIR, ".env")

load_dotenv(dotenv_path=ENV_FILE)



def create_app():
    app = Flask(__name__)

    return app