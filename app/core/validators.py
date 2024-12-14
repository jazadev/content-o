from flask import jsonify



def get_validation_error(data):
    # TODO: raise if id_email is not present
    if data.get("query", False) is False:
        return jsonify({"error": "query field is missing"}), 400

    return False