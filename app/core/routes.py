import logging
import json
from flask import request, jsonify, Blueprint, redirect, request, jsonify
from app.core.validators import get_validation_error
from app.core.utils import process_user, process_anonimous, get_user_groups
import os
import jwt
import requests
from functools import wraps

routes_core = Blueprint('core', __name__)

# Configuración de Azure Entra ID
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
TENANT_ID = os.environ.get("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
JWKS_URL = f"https://login.microsoftonline.com/common/discovery/keys"
ALLOWED_ROLES = ["Admin", "Member"]  # Roles permitidos
REDIRECT_URI = "http://localhost:5000/api/v1/callback"
SECRET= os.environ.get("SECRET")


# Cache de las claves públicas
jwks = {}

# Función para obtener y almacenar las claves públicas
def get_jwks():
    global jwks
    if not jwks:
        try:
            response = requests.get(JWKS_URL)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            jwks = response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch JWKS: {str(e)}")
            return {}
        except ValueError as e:
            logging.error("Invalid JSON response for JWKS")
            return {}
    return jwks

@routes_core.route("/content-o-courses", methods=["POST"])
def content_o_courses():
    data = request.json

    error = get_validation_error(data=data)
    if error:
        return error

    try:
        response = process_anonimous(data)
        response_data = {
            "stage_duration": response.get('stage_duration', []),
            "stage_token_usage": response.get('stage_token_usage', []),
            "role": response.get('role', ''),
            "content": response['response_data'].choices[0].message.content,
            "usage": {
                "completion_tokens": response['response_data'].usage.completion_tokens,
                "prompt_tokens": response['response_data'].usage.prompt_tokens,
                "total_tokens": response['response_data'].usage.total_tokens
            }
        }
        return jsonify({"message": "Public endpoint accessed", "data": response_data}), 200
    except Exception as e:
        logging.exception(str(e))
        return jsonify({"error": str(e)}), 500

@routes_core.route("/content-o-members", methods=["POST"])
def content_o_members():
    auth_header = request.headers.get("Authorization")
    access_token = request.headers.get("X-Access-Token")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "No valid token provided"}), 401

    token = auth_header.split(" ")[1]
    
    try:
        # Get the token header to extract kid
        header = jwt.get_unverified_header(token)
        kid = header['kid']
        token_url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
        
        # Get JWKS from Microsoft
        jwks_url = f'https://login.microsoftonline.com/common/discovery/v2.0/keys'
        jwks_response = requests.get(jwks_url)
        jwks = jwks_response.json()
        
     
        # Find the signing key
        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
        if not key:
            return jsonify({"error": "Invalid token: Key not found"}), 401
            
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        
        # Verify the token
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=f"https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/v2.0"
        )
        
        member = decoded_token.get('email', [])
        
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': SECRET,
            'scope': 'https://graph.microsoft.com/.default'
            }
        
        # Solicitar token
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        access_token = response.json().get('access_token')
        
        print(f"Access Token: {access_token}")
        
        
        if member:
            groups = get_user_groups(access_token,member)
        
        data = request.json
        if not data or "query" not in data:
            return jsonify({"error": "'query' is required"}), 400

        response = process_user(data, groups)
        try:
            content = response['response_data'].choices[0].message.content 
        except Exception as e:
            content = response['response_data']
        
        usage_data = {
            "completion_tokens": response['response_data'].usage.completion_tokens if hasattr(response['response_data'], 'usage') and hasattr(response['response_data'].usage, 'completion_tokens') else 0,
            "prompt_tokens": response['response_data'].usage.prompt_tokens if hasattr(response['response_data'], 'usage') and hasattr(response['response_data'].usage, 'prompt_tokens') else 0,
            "total_tokens": response['response_data'].usage.total_tokens if hasattr(response['response_data'], 'usage') and hasattr(response['response_data'].usage, 'total_tokens') else 0
        }
        
        response_data = {
            "stage_duration": response.get('stage_duration', []),
            "stage_token_usage": response.get('stage_token_usage', []),
            "role": response.get('role', ''),
            "content":content,
            "usage": usage_data
        }
        return jsonify({"message": "Premium endpoint accessed", "data": response_data}), 200
    

    except jwt.InvalidTokenError as e:
        return jsonify({"error": f"Invalid token: {str(e)}"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@routes_core.route("/login/microsoft", methods=["GET"])
def microsoft_login():
    auth_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "id_token token",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email User.Read GroupMember.Read.All Directory.Read.All",
        "response_mode": "fragment",
        "state": "12345",
        "nonce": "678910"
    }
    
    # Use requests.utils.quote to properly encode the parameters
    from urllib.parse import urlencode
    full_auth_url = f"{auth_url}?{urlencode(params)}"
    return redirect(full_auth_url)


@routes_core.route("/callback")
def callback():
    return """
        <script>
            const hash = window.location.hash.substring(1);
            const params = new URLSearchParams(hash);
            const idToken = params.get('id_token');
            const accessToken = params.get('access_token');
            
            if (idToken && accessToken) {
                localStorage.setItem('id_token', idToken);
                localStorage.setItem('access_token', accessToken);
                window.location.href = '/members';
            } else {
                window.location.href = '/login';
            }
        </script>
    """