import logging

from flask import request, jsonify, Blueprint
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
TENANT_ID = os.environ.get("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
JWKS_URL = f"{ISSUER}/discovery/v2.0/keys"
ALLOWED_ROLES = ["Admin", "Member"]  # Roles permitidos


# Cache de las claves públicas
jwks = {}

# Función para obtener y almacenar las claves públicas
def get_jwks():
    global jwks
    if not jwks:
        response = requests.get(JWKS_URL)
        jwks = response.json()
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
        return jsonify({"message": "Public endpoint accessed", "data": data}), 200
    except Exception as e:
        logging.exception(str(e))
        return jsonify({"error": str(e)}), 500


@routes_core.route("/content-o-members", methods=["POST"])
@require_auth(required_roles=ALLOWED_ROLES)
def process_complete():
    data = request.json

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    query = data.get("query")

    if query is None:
        return jsonify({"error": "'query' is required"}), 400

    try:
        message = "ok"
        return jsonify({"message": message}), 200
    except Exception as e:
        logging.exception("An error occurred while processing the request")
        return jsonify({"error": f"The request cannot be completed, {str(e)}"}), 500