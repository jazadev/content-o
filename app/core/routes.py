import logging
import json
from flask import request, jsonify, Blueprint, render_template, send_from_directory, redirect
from app.core.validators import get_validation_error
from app.core.utils import process_user, process_anonimous
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import msal

import os
import jwt
import requests
from flask import Flask, request, jsonify
from functools import wraps

routes_core = Blueprint('core', __name__)

# Configuración de Azure Entra ID
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
TENANT_ID = os.environ.get("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
ISSUER = f"https://login.microsoftonline.com/common/v2.0"
JWKS_URL = f"https://login.microsoftonline.com/common/discovery/keys"
ALLOWED_ROLES = ["Admin", "Member"]  # Roles permitidos
REDIRECT_URI = "http://localhost:5000/api/v1/callback"


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


# Decorador para validar tokens y roles
def require_auth(required_roles=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", None)
            if not auth_header:
                return jsonify({"error": "Authorization header is missing"}), 401

            token = auth_header.split(" ")[1] if " " in auth_header else auth_header

            try:
                # Obtener claves públicas (JWKS) y validar el token
                jwks = get_jwks()
                
                if not jwks or "keys" not in jwks:
                    return jsonify({"error": "Unable to fetch JWKS for token validation"}), 500

                decoded_token = jwt.decode(
                    token,
                    key=lambda header, _: jwt.algorithms.RSAAlgorithm.from_jwk(
                        next(
                            key for key in jwks["keys"]
                            if key["kid"] == header["kid"]
                        )
                    ),
                    algorithms=["RS256"],
                    audience=CLIENT_ID,
                    issuer=ISSUER,
                )

                # Validar roles si es necesario
                roles = decoded_token.get("roles", [])
                if required_roles and not any(role in roles for role in required_roles):
                    return jsonify({"error": "Access denied: insufficient role"}), 403

                # Token válido y rol aceptado
                return f(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return wrapper
    return decorator


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
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "No valid token provided"}), 401

    token = auth_header.split(" ")[1]
    
    try:
        # Get the token header to extract kid
        header = jwt.get_unverified_header(token)
        kid = header['kid']
        
        # Get JWKS from Microsoft
        jwks_url = f'https://login.microsoftonline.com/common/discovery/v2.0/keys'
        jwks_response = requests.get(jwks_url)
        jwks = jwks_response.json()
        
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        print("importante")
        print(unverified_payload.get("iss"))

        
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
        data = request.json
        if not data or "query" not in data:
            return jsonify({"error": "'query' is required"}), 400

        response = process_user(data)
        return jsonify({"message": "Premium endpoint accessed", "data": response}), 200

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
        "scope": "openid profile User.Read",
        "response_mode": "fragment",
        "state": "12345",
        "nonce": "678910"
    }
    
    full_auth_url = f"{auth_url}?{'&'.join(f'{k}={v}' for k,v in params.items())}"
    return redirect(full_auth_url)

@routes_core.route("/callback")
def callback():
    return """
        <script>
            const hash = window.location.hash.substring(1);
            const params = new URLSearchParams(hash);
            const access_token = params.get('id_token'); // Changed from access_token to id_token
            if (access_token) {
                localStorage.setItem('token', access_token);
                window.location.href = '/members';
            } else {
                window.location.href = '/login';
            }
        </script>
    """
