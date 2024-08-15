from flask import Flask
from .modules.user_table import add_user

app = Flask(__name__)


@app.route('/add_user', methods=['POST'])
def add_user_route():
    return add_user()


if __name__ == "__main__":
    app.run()

