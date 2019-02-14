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


@app.route('/home/')
def display_home():
    # used to see home
    return render_template('home.html')


@app.route('/get_title/', methods=['GET'])
def get_title():
    connexion.send('get title')
    title = connexion.recv()
    return title


@app.route('/search/<research>', methods=['POST'])
def search(research):
    if '$' == research[0]:
        # used to execute command directly from the web interface
        connexion.send(research[1:])
    else:
        connexion.send('search:{}:0'.format(research))
    return 'done'


def error_page():
    return render_template('error.html')


if __name__ == "__main__":
    app.run()
