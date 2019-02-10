from flask import Flask
from flask import render_template
# from multiprocessing.connection import Client

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/you')
def get_ses():
    # try:
    #     address = ('localhost', 6003)
    #     conn = Client(address, authkey=b'secret password')
    # except:
    #     address = ('localhost', 6004)
    #     conn = Client(address, authkey=b'secret password')
    #
    # conn.send('lalalallalallalalalalalalala')

    print('done')
    return 'hi'
