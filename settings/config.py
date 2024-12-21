import os

from dotenv import load_dotenv
from flask import Flask


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_FILE = os.path.join(ROOT_DIR, ".env")

load_dotenv(dotenv_path=ENV_FILE)

# Used by the OpenAI SDK
AZURE_OPENAI_API_TYPE = os.getenv("AZURE_OPENAI_API_TYPE")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


AZURE_STORAGE_ACCOUNT_CONNECTION_STRING=DefaultEndpointsProtocol=os.getenv("AZURE_STORAGE_ACCOUNT_CONNECTION_STRING")
AZURE_STORAGE_ACCOUNT_KEY=os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
AZURE_STORAGE_CONTAINER_NAME=os.getenv("AZURE_STORAGE_CONTAINER_NAME")


AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
CONTENT_SAFETY_ENDPOINT=os.getenv("CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY= os.getenv("CONTENT_SAFETY_KEY")

class ConfigContento:
    JSON_SORT_KEYS = False

def create_app(config_class=ConfigContento):
    app = Flask(__name__)
    app.config.from_object(config_class)

    return app