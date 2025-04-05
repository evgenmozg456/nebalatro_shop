from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Магазин Небалатро"


@app.route('/kick_timatun')
def index():
    return "kick timatun5000!"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
