import sys

sys.path.insert(0, "/home/rengati/random_music_wizard/")  # WARNING depends on path
from flask import Flask
from flask import render_template, request
from multiprocessing.connection import Client
from communication import Connexion
from time import sleep

app = Flask(__name__)
connexion = None
connexion_receiver = None


def connect():
    try:
        address = ('localhost', 6003)
        new_connexion = Client(address, authkey=b'secret password')
    except:
        address = ('localhost', 6004)
        new_connexion = Client(address, authkey=b'secret password')

    new_connexion_receiver = Connexion.Connexion(new_connexion)
    new_connexion_receiver.start()

    return new_connexion, new_connexion_receiver


@app.route("/")
def home():
    global connexion, connexion_receiver

    if not connexion:
        try:
            connexion, connexion_receiver = connect()
        except:
            return error_page()

    return render_template('home.html')


@app.route("/pause/", methods=['POST'])
def pause():
    connexion.send('pause')
    app.logger.error('PAUSE')
    return 'done'


@app.route("/play/", methods=['POST'])
def play():
    connexion.send('play')
    return 'done'


@app.route("/next/", methods=['POST'])
def next():
    connexion.send('next')
    return 'done'


@app.route('/like/', methods=['POST'])
def like():
    connexion.send('like')
    return 'done'


@app.route('/volume_up/', methods=['POST'])
def volume_up():
    connexion.send('++')
    return 'done'


@app.route('/volume_down/', methods=['POST'])
def volume_down():
    connexion.send('--')
    return 'done'


@app.route('/home/')
def display_home():
    # used to see home
    return render_template('home.html')


@app.route('/get_title/', methods=['POST'])
def get_title():
    title = connexion_receiver.last_message_received
    app.logger.error("TITLE: " + str(title))
    app.logger.error("RECEIVER ALIVE" + str(connexion_receiver.is_open))
    return title


@app.route('/search/<research>', methods=['POST'])
def search(research):
    if '$' == research[0]:
        # used to execute command directly from the web interface
        connexion.send(research[1:])
    else:
        connexion.send('search:{}:1'.format(research))
    return 'done'


def error_page():
    return render_template('error.html')


if __name__ == "__main__":
    app.run()
