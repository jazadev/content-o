import requests

#from services.azure_cosmosdb import CosmosDB
from services.azure_openai.main import ChatGPTService

from settings.config import (
    AZURE_STORAGE_ACCOUNT_CONNECTION_STRING, 
    AZURE_STORAGE_CONTAINER_NAME, 
    #AZURE_STORAGE_CSV
)
from services.azure_openai.utils import read_csv, search_word



def process_user(data, role):
    query = data.get("query")


    #store_service = StorageAccount(AZURE_STORAGE_ACCOUNT_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_NAME)
    #list_files_to_identifier = store_service.get_files_list(filter_name=primary_key)

    chatgpt_connection = ChatGPTService()
    response = chatgpt_connection.process(query=query,role=role)

    
    return response


def process_anonimous(data):
    query = data.get("query")


    #store_service = StorageAccount(AZURE_STORAGE_ACCOUNT_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_NAME)
    #list_files_to_identifier = store_service.get_files_list(filter_name=primary_key)

    chatgpt_connection = ChatGPTService()
    response = chatgpt_connection.process_anon(query=query)
    
    return response