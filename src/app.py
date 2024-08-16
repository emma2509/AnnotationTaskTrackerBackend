from flask import Flask
from .modules.user_table import add_user
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/add_user', methods=['POST'])
def add_user_route():
    return add_user()


if __name__ == "__main__":
    app.run()

