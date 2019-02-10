from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Flask!"


@app.route("/you/")
def you():
    return "Hello, you!"


if __name__ == "__main__":
    app.run()
