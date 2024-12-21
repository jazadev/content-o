import requests
import json
from services.azure_openai.main import ChatGPTService


def get_user_groups(access_token, user_id):
    graph_url = f'https://graph.microsoft.com/v1.0/users'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("Access Token:", access_token)
        response = requests.get(
            graph_url,
            headers=headers,
            params={'$select': 'displayName,id,mail,groups'}
        )
  
        print(f"Graph API Response: {response.status_code} - {response.text}")
        
        response.raise_for_status()
        data = json.loads(response.text)
        
        usuario = next((user for user in data['value'] if user.get('mail') == user_id), None)
        
        if usuario:
            print(f"Usuario encontrado: {usuario}")
        else:
            print("Usuario no encontrado")
            
        id_usuario = usuario['id']

        headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
        }
        
        groups_url = f'https://graph.microsoft.com/v1.0/users/{id_usuario}/memberOf'
        groups_response = requests.get(groups_url, headers=headers, params={'$select': 'displayName,id'})
        groups_data = groups_response.json().get('value', [])

    
        print(groups_data)
        security_groups = [
            group['displayName'] for group in groups_data 
            if group.get('@odata.type', '') == '#microsoft.graph.group'
        ]
        
        return security_groups[0]
    except Exception as e:
        print(f"Error fetching groups: {e}")
        return []



def process_user(data, group_name):
    query = data.get("query")
    chatgpt_connection = ChatGPTService()
    response = chatgpt_connection.process(query=query,role=group_name)
    return response


def process_anonimous(data):
    query = data.get("query")
    chatgpt_connection = ChatGPTService()
    response = chatgpt_connection.process_anon(query=query)
    return response