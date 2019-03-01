import sys

sys.path.insert(0, "/home/rengati/random_music_wizard/")  # WARNING depends on path
from flask import Flask
from flask import render_template, request
from communication import ServerClient


app = Flask(__name__)

server_client = ServerClient.ServerClient(app.logger)


@app.route("/")
def home():
    success = server_client.connect()

    if success:
        return render_template('home.html')
    return error_page()


@app.route("/pause/", methods=['POST'])
def pause():
    server_client.send('pause')
    return 'done'


@app.route("/play/", methods=['POST'])
def play():
    server_client.send('play')
    return 'done'


@app.route("/next/", methods=['POST'])
def next():
    server_client.send('next')
    return 'done'


@app.route('/like/', methods=['POST'])
def like():
    server_client.send('like')
    return 'done'


@app.route('/volume_up/', methods=['POST'])
def volume_up():
    server_client.send('++')
    return 'done'


@app.route('/volume_down/', methods=['POST'])
def volume_down():
    server_client.send('--')
    return 'done'


@app.route('/home/')
def display_home():
    # used to see home
    return render_template('home.html')


@app.route('/get_title/', methods=['POST'])
def get_title():
    title = server_client.get_title()
    app.logger.error("TITLE: " + str(title))
    # app.logger.error("RECEIVER ALIVE: " + str(connection_receiver.is_open))

    return title


@app.route('/search/<research>', methods=['POST'])
def search(research):
    if '$' == research[0]:
        # used to execute command directly from the web interface
        server_client.send(research[1:])
    else:
        server_client.send('search:{}:1'.format(research))
    return 'done'


def error_page():
    return render_template('error.html')


if __name__ == "__main__":
    app.run()
