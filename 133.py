from flask import Flask
from flask_restful import Api
from data import db_session
from data.comments import Comment


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/nebalatro.db")
    # 1
    com = Comment()
    com.text = 'Игра плохая 0/10'
    com.user_id = 1
    com.game_id = 10000000
    db_sess = db_session.create_session()
    db_sess.add(com)
    db_sess.commit()

    com = Comment()
    com.text = 'Игра ужасная 3/10'
    com.user_id = 2
    com.game_id = 10000000
    db_sess = db_session.create_session()
    db_sess.add(com)
    db_sess.commit()
    # 3
    com = Comment()
    com.text = 'Игра гуд 13/10'
    com.user_id = 2
    com.game_id = 10000000
    db_sess = db_session.create_session()
    db_sess.add(com)
    db_sess.commit()

if __name__ == '__main__':
    main()
