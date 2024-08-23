from flask import Flask
from .modules.user_table import add_user, get_user_password, get_users
from .modules.annotation_table import get_all_annotations, add_annotation_task
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/add_user', methods=['POST'])
def add_user_route():
    return add_user()


@app.route('/get_user_password', methods=['POST'])
def get_user_password_route():
    return get_user_password()


@app.route('/get_users', methods=['GET'])
def get_users_route():
    return get_users()


@app.route('/get_annotations', methods=['GET'])
def get_annotations_route():
    return get_all_annotations()


@app.route('/add_annotation', methods=['POST'])
def add_annotation_route():
    return add_annotation_task()


if __name__ == "__main__":
    app.run()
