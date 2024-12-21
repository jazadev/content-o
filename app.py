from flask import jsonify, make_response, render_template, send_from_directory
import os
from app.core.routes import routes_core
from settings.config import create_app


app = create_app()
app.register_blueprint(routes_core, url_prefix='/api/v1/')


# Set absolute paths for templates and static folders
base_dir = os.path.abspath(os.path.dirname(__file__))
app.template_folder = os.path.join(base_dir, 'templates')
app.static_folder = os.path.join(base_dir, 'static')


@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


@app.route("/hello", methods=["GET"])
def hello():
    message = jsonify({"message": "Hello, World!"})
    return make_response(message, 200)

@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/members')
def members_page():
    return render_template('members.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)