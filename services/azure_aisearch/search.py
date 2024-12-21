import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Configuración de Azure Cognitive Search
search_service_name = os.environ.get("AI_SEARCH_SERVICE_NAME")
index_name = 'documents'
api_key = os.environ.get("AI_SEARCH_API_KEY")

search_url = f'https://{search_service_name}.search.windows.net/indexes/{index_name}/docs'

# Función para realizar una consulta de búsqueda
def search_documents(query):
    # Parámetros de la consulta
    params = {
        'api-version': '2024-07-01',
        'search': query,
        '$top': 3  # Limitar a 1 resultado más relevante
    }

    # Cabeceras de autenticación
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }

    # Realizar la solicitud POST
    response = requests.get(search_url, params=params, headers=headers)

    if response.status_code == 200:
        # Obtener los resultados
        results = response.json().get('value', [])

        if results:
            # Extraer el contenido del primer resultado
            document = results[0]
            return str(document)  # Devuelve el documento encontrado
        else:
            return 'Lo siento, no encontré ninguna respuesta.'
    else:
        # Si ocurre un error en la solicitud
        return f'Error al buscar: {response.status_code} - {response.text}'

# Función para manejar la consulta del usuario
def handle_user_query(user_query):
    result = search_documents(user_query)
    return result

