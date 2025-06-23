# <-***** flask (2010) [1] - START
from flask import Flask
# ->***** flask (2010) [1] - END

from .modules.authentication import authenticate
from .modules.user_table import (
    add_user,
    get_users,
)
from .modules.annotation_table import (
    get_all_annotations,
    add_annotation_task,
    update_annotation_record,
    delete_annotation_record,
)
# <-***** flask-cors (2025) [4] - START
from flask_cors import CORS
# ->***** flask-cors (2025) [4] - END

app = Flask(__name__)
CORS(app)


@app.route("/log_in", methods=["POST"])
def log_in_route():
    return authenticate()


@app.route("/add_user", methods=["POST"])
def add_user_route():
    return add_user()


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
