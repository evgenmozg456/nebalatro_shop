# from flask import Flask, render_template
#
# app = Flask(__name__)
#
#
# @app.route('/')
# @app.route('/home')
# def home():
#     return render_template('home.html')
#
#

#
#
# if __name__ == '__main__':
#     app.run(port=8080, host='127.0.0.1')
import flask
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'button_reg' in request.form:
            return redirect('/register')
        elif 'button_sign' in request.form:
            return redirect('/signin')
        elif 'button_about' in request.form:
            return redirect('/about')
    return render_template('home.html')

@app.route('/kick_timatun')
def kick_timatun():
    return render_template('kick_timatun.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/signin')
def sign_in():
    return render_template('sign_in.html')

@app.route('/about')
def about_us():
    return render_template('about_us.html')



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
