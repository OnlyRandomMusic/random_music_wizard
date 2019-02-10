from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, new Flask!"


@app.route("/you/")
def you():
    return "Hello, new you!"


if __name__ == "__main__":
    app.run()
