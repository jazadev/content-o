import json
import datetime
from functools import wraps
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
import os
import logging
from urllib.parse import quote_plus
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
#import openai get_prompt
from openai import AzureOpenAI  # New import style
from services.azure_aisearch.search import handle_user_query
from services.azure_content_safety.content_safety import validate_with_content_safety, Action
from tenacity import retry, wait_random_exponential, stop_after_attempt
from services.azure_openai.utils import is_query_allowed
from langchain_openai import AzureChatOpenAI
from settings.config import (
    AZURE_OPENAI_API_BASE,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    CONTENT_SAFETY_ENDPOINT,
    CONTENT_SAFETY_KEY
)
from services.azure_openai.utils import (
    get_prompt,
    get_usage_tokens,
)
endpoint = CONTENT_SAFETY_ENDPOINT
subscription_key = CONTENT_SAFETY_KEY
api_version = "2024-09-01"
OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_API_BASE")
AZURE_DEPLOYMENT_NAME = "gpt-4o-mini"
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")

# Configuración de la conexión a Azure SQL
SERVER = os.environ.get("SERVER")
DATABASE = os.environ.get("DATABASE")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
ENGINE_MODEL_VERSION = "gpt-4o-mini"

connection_string = f"mssql+pyodbc://{quote_plus(USERNAME)}:{quote_plus(PASSWORD)}@{SERVER}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server&connect_timeout=30&connection_timeout=30"

def measure_time(stage_name):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, *args, **kwargs):
            t1 = datetime.datetime.now()
            result = func(cls, *args, **kwargs)
            elapsed_time = (datetime.datetime.now() - t1).total_seconds()
            cls.stage_duration.append({stage_name: elapsed_time})
            return result
        return wrapper
    return decorator


class ChatGPTService:

    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_API_BASE
        )
        
        self.stages_engine_version = ENGINE_MODEL_VERSION
        self.stage_duration = []
        self.stage_token_usage = []
        self.conversation_history = []
        self.current_role = None

    def start_conversation(self, role):
        """Initialize conversation with role-specific system prompt"""
        self.current_role = role
        if role != None:
            prompt = get_prompt(role.strip())
        else:
            prompt = get_prompt("external-user")
        self.conversation_history = [
            {"role": "system", "content": prompt}
        ]

    @retry(wait=wait_random_exponential(min=2, max=60), stop=stop_after_attempt(3), reraise=True)
    def run_query_chatgpt(self, query, source, role=None):
        try:
            
            # If role changes or conversation not started, initialize with new role
            if role != self.current_role or not self.conversation_history:
                self.start_conversation(role)

            #tools = get_tools(role)
            engine_version = "gpt-4o-mini"

            prompt = source +'/n'+ 'Pregunta: ' + query 

            # Add user message while maintaining the system prompt
            self.conversation_history.append({"role": "user", "content": prompt})



            completion = self.client.chat.completions.create(
                model=engine_version,
                messages=self.conversation_history,
                temperature=0,
                max_tokens=3000,
                top_p=0.9
            )

            assistant_message = completion.choices[0].message
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content if assistant_message.content else "",
                "tool_calls": assistant_message.tool_calls
            })
            print(assistant_message.content)


            token_consumed = {role: get_usage_tokens(completion)}
            self.stage_token_usage.append(token_consumed)
        except Exception as e:
            # TODO: delete after testing, and logging
            print(f"Error in ChatGPT request. Detail: {e}")
            completion = {}

        return completion



    def process(self, role, query):
        try:
            engine = create_engine(connection_string)
            db = SQLDatabase(engine)
            print("Conexión a la base de datos exitosa")
            
            llm = AzureChatOpenAI(
                api_key=OPENAI_API_KEY,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                deployment_name=AZURE_DEPLOYMENT_NAME,
                api_version=AZURE_OPENAI_API_VERSION,
                model_name="gpt-4o-mini"
            )
            
            # Crea un agente para consultas SQL
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            
            agent = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                verbose=True,
            )
            
            if validate_with_content_safety(query, endpoint, subscription_key, api_version,).suggested_action == Action.Reject:
                response_data= "Consulta denegada: el contenido de entrada es inapropiado."
            elif not is_query_allowed(query, role):
                response_data= f"Permiso denegado: el rol '{role}' no tiene acceso a esta consulta."
            else:
                response = agent.run(query)
                #documents = handle_user_query(query)
                response_data = self.run_query_chatgpt(query=query, source=response, role=role)
            
            print(response_data)


        #except openai.error.InvalidRequestError as e:
        #   return {"error": "Maximum token length exceeded. Please reduce the length of the input text."}
        except Exception as e:
            print(f"Error processing the request. Detail: {e}")
            return {"error": f"Error processing the request {e}"}

        try:
            messages = {
                "stage_duration": self.stage_duration,
                "stage_token_usage": self.stage_token_usage,
                "role": role.strip(),
                "response_data": response_data,
            }
        except Exception as e:
            print(f"JSON encoding error. Detail: {e}")
            messages = {
                "error": "JSON encoding error"
            }

        return messages
    
    def process_anon(self, query):
        try:

            documents = handle_user_query(query)

            response_data = self.run_query_chatgpt(query=query, source=documents)
            
            print(response_data)

        except Exception as e:
            print(f"Error processing the request. Detail: {e}")
            return {"error": f"Error processing the request {e}"}

        try:
            messages = {
                "stage_duration": self.stage_duration,
                "stage_token_usage": self.stage_token_usage,
                "role": "not user",
                "response_data": response_data,
            }
        except Exception as e:
            print(f"JSON encoding error. Detail: {e}")
            messages = {
                "error": "JSON encoding error"
            }

        return messages