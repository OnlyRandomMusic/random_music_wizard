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
            return render_template('no_instance.html')


@app.route("/play")
def play():
    return 'playing'


@app.route('/you/')
def get_ses():
    connexion.send('lalalallalallalalalalalalala')

    print('done')
    return 'hi'


if __name__ == "__main__":
    app.run()
