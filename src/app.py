from flask import Flask
from .modules.user_table import (
    add_user,
    get_user_password,
    get_users,
    get_user_access_level,
)
from .modules.annotation_table import (
    get_all_annotations,
    add_annotation_task,
    update_annotation_record,
    delete_annotation_record,
)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/add_user", methods=["POST"])
def add_user_route():
    return add_user()


@app.route("/get_user_password", methods=["POST"])
def get_user_password_route():
    return get_user_password()


@app.route("/get_user_access_level", methods=["POST"])
def get_user_access_route():
    return get_user_access_level()


@app.route("/get_users", methods=["GET"])
def get_users_route():
    return get_users()


@app.route("/get_annotations", methods=["GET"])
def get_annotations_route():
    return get_all_annotations()


@app.route("/add_annotation", methods=["POST"])
def add_annotation_route():
    return add_annotation_task()


@app.route("/update_annotation", methods=["POST"])
def update_annotation_route():
    return update_annotation_record()


@app.route("/delete_annotation", methods=["POST"])
def delete_annotation_route():
    return delete_annotation_record()


if __name__ == "__main__":
    app.run()
