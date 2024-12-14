from flask import jsonify, make_response, redirect, url_for

from app.core.routes import routes_core
from settings.config import create_app


app = create_app()
app.register_blueprint(routes_core, url_prefix='/api/v1/')


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for('hello'))


@app.route("/hello", methods=["GET"])
def hello():
    message = jsonify({"message": "Hello, World!"})
    return make_response(message, 200)


if __name__ == "__main__":
    app.run(debug=True)