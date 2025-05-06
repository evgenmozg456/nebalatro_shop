import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import *
# pip install SQLAlchemy-serializer

class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    reply_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    data = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now().date())
    like_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    liked_id = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')

# .strftime('%d.%m.%Y %H:%M')