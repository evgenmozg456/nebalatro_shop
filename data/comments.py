import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import *


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
