from flask import Flask
from flask import render_template
from multiprocessing.connection import Client

app = Flask(__name__)
connexion = None


def connect():
    try:
        address = ('localhost', 6003)
        new_connexion = Client(address, authkey=b'secret password')
    except:
        address = ('localhost', 6004)
        new_connexion = Client(address, authkey=b'secret password')

    return new_connexion


@app.route("/")
def home():
    global connexion

    if not connexion:
        try:
            connexion = connect()
            return render_template('home.html')
        except:
            return error_page()

    else:
        return render_template('home.html')


@app.route("/pause/")
def pause():
    connexion.send('pause')


@app.route("/play/")
def play():
    connexion.send('play')


@app.route("/next/")
def next():
    connexion.send('next')


@app.route('/like/')
def like():
    connexion.send('like')


def error_page():
    return render_template('error.html')


if __name__ == "__main__":
    app.run()
