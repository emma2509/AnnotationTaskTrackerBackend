from flask import Flask
from .modules.user_table import add_user, get_user_password
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/add_user', methods=['POST'])
def add_user_route():
    return add_user()


@app.route('/get_user', methods=['GET'])
def get_user_route():
    return get_user_password()


if __name__ == "__main__":
    app.run()

