from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/kick_timatun')
def index():
    return render_template('kick_timatun.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
