import sqlalchemy
from sqlalchemy_serializer import *
from data.db_session import SqlAlchemyBase


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    steam_id = sqlalchemy.Column(sqlalchemy.Integer)
