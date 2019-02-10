from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, the best Flask!"


@app.route("/you/")
def you():
    return "Hello, the best you!"


if __name__ == "__main__":
    app.run()
