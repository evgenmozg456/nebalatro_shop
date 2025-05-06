import os

import flask_login
from flask import Flask, render_template, request, redirect, abort, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from data import db_session
from data.comments import Comment
from data.users import User
from data.game import Game
from forms.finder_form import FindForm
from forms.loginform import LoginForm
from forms.redact_form import RedactForm
from forms.user_form import RegisterForm
from forms.comment_form import CommentForm
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static'
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = FindForm()
    if request.method == 'POST':
        if 'button_reg' in request.form:
            return redirect('/registration_test')
        elif 'button_sign' in request.form:
            return redirect('/login')
        elif 'button_about' in request.form:
            return redirect('/about')
        elif 'find' in request.form:
            game_name = request.form['game_name']
            # print(game_name)
            return redirect('/game')
    return render_template('home.html', form=form)


@app.route('/kick_timatun')
def kick_timatun():
    return render_template('kick_timatun.html')


@app.route('/game/<game_id>')
def game_card(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == game_id).first()
    return render_template('game_card.html', game=game)

@app.route('/signin')
def sign_in():
    return render_template('sign_in.html')


@app.route('/about')
def about_us():
    return render_template('about_us.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('testing_login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('testing_login.html', title='Авторизация', form=form)


@app.route('/registration_test', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('testing_reg.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('testing_reg.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('testing_reg.html', title='Регистрация', form=form)


@app.route('/profile')
def profile():
    cur_user = flask_login.current_user
    if current_user.is_authenticated:
        return render_template('profile.html',
                               created_date=cur_user.created_date, name=cur_user.name, about=cur_user.about)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/comments_list', methods=['GET', 'POST'])
def comments_list():
    db_sess = db_session.create_session()
    comments = db_sess.query(Comment).filter(Comment.reply_id == 0).all()
    coms = []
    for i in comments:
        user_name = db_sess.query(User).filter(User.id == i.user_id).first()
        coms.append([i.id, i.text, user_name.name, i.data, i.reply_id, i.game_id, 0, get_comment_rec(db_sess, i.id, 1), i.user_id])
    return render_template('comments_list_test.html', title= 'Комменты', form= coms)


def get_comment_rec(db_sess, id_parent, level=0):
    comments = db_sess.query(Comment).filter(Comment.reply_id == id_parent).all()

    if not comments:
        return ''
    else:
        coms = ''
        for i in comments:
            user_name = db_sess.query(User).filter(User.id == i.user_id).first()
            s = f"""
            <p>
                <p style="margin-left: {50*level}px; border:5px; border-style:inset; border-color:pink; padding: 1em; border-radius: 30px;">
                Имя пользователя:{user_name.name}<br>
                Комментарий:{i.text}<br>
                Дата отправки:{i.data}<br>
                <a class="nav-button" href="/comment/{i.id}/{i.game_id}/{i.user_id}">Ответить</a>

                </p>
            </p>
            """
            coms += s
            if i.reply_id != 0:
                coms+= get_comment_rec(db_sess, i.id, level+1)
            # coms.append([i.id, i.text, user_name.name, i.data, i.reply_id, i.game_id, level+1, get_comment_rec(session, i.id, level+1)])
        return coms




@app.route('/comment/<int:reply_id>/<int:game_id>/<int:user_id>', methods=['GET', 'POST'])
def comment(reply_id,game_id, user_id):
    form = CommentForm()
    if form.validate_on_submit():
        print(reply_id)
        com = Comment()
        com.text = request.form.get('text')
        com.user_id = user_id
        com.game_id = game_id
        com.reply_id = reply_id
        db_sess = db_session.create_session()
        db_sess.add(com)
        db_sess.commit()
        return redirect('/comments_list')
    return render_template('LeaveComment.html', title='Комментарий', form=form, reply_id = reply_id,game_id=game_id )


@app.route('/profile_redact', methods=['GET', 'POST'])
def profile_redact():
    form = RedactForm()
    cur_user = flask_login.current_user
    db_sess = db_session.create_session()
    if form.validate_on_submit():

        user = db_sess.query(User).filter(User.id == cur_user.id).first()

        if user:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(user.id) + ".jpg")
            form.avatar.data.save(file_path)
            user.name = form.name.data
            user.about = form.about.data
            db_sess.commit()
            return redirect("/profile")
    return render_template('redact.html', title='Регистрация', form=form)



# так называемый поиск

@app.route('/game', methods=['GET', 'POST'])
def search():
    try:
        db_sess = db_session.create_session()
        search_term = request.args.get('game_name', '').strip()

        if not search_term:
            return render_template('game.html', error="Введите название игры")

        games = db_sess.query(Game).filter(Game.name.ilike(f'%{search_term}%')).all()
        print(games)

        if not games:
            return render_template('game.html',
                                   error=f"Игра '{search_term}' не найдена",
                                   search_term=search_term)

        main_game = games[0]
        similar_games = games[1:] if len(games) > 1 else []

        return render_template('game.html',
                               main_game=main_game,
                               similar_games=similar_games,
                               search_term=search_term)

    except Exception as e:
        print(f'Ошибка при поиске: {str(e)}')
        return render_template('game.html',
                               error=f"Произошла ошибка при поиске: {str(e)}")



def main():
    db_session.global_init("db/nebalatro.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()
