from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to My Flask Web Application!"


if __name__ == "__main__":
    app.run()

