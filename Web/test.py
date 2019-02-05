from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

from flask import render_template

@app.route('/hello/')
def hello_page():
    return render_template('index.html')

@app.route('/hello/you')
def get_ses():
    print('done')
    return hello_page()



