import logging

from flask import request, jsonify, Blueprint
from app.core.validators import get_validation_error


routes_core = Blueprint('core', __name__)


@routes_core.route("/content-o-courses", methods=["POST"])
def content_o_courses():
    data = request.json

    error = get_validation_error(data=data)
    if error:
        return error

    try:
        response = "ok"
        return jsonify({"message": response}), 200
    except Exception as e:
        logging.exception(str(e))
        return jsonify({"error": str(e)}), 500


@routes_core.route("/content-o-members", methods=["POST"])
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