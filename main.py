from flask import Flask

app: Flask = Flask(__name__)

@app.get('/')
def index():
    return '<h1>Hello World !</h1>'
