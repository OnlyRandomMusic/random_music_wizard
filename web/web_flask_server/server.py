import sys

sys.path.insert(0, "/home/rengati/random_music_wizard/")  # WARNING depends on path
from flask import Flask
from flask import render_template, request
from multiprocessing.connection import Client


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

    # new_connexion_receiver = Process(target=receive, args=(new_connexion,))
    # new_connexion_receiver.daemon = True
    # new_connexion_receiver.start()

    return new_connexion


def receive(connexion):
    while True:
        # try:
        message = connexion.recv()

        app.logger.error("MESSAGE RECEIVED: " + message)
        # except:
        #     sleep(0.5)
        # self.connexion.close()
        # break

    self.is_open = False


@app.route("/")
def home():
    global connexion

    if not connexion:
        try:
            connexion = connect()
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
    connexion.send('get_title')
    title = connexion.recv()
    app.logger.error("TITLE: " + str(title))
    # app.logger.error("RECEIVER ALIVE: " + str(connexion_receiver.is_open))

    if title:
        return title
    return "no title"


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
