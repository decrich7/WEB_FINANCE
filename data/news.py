import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_portfel = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    horiz = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    short = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_file = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    tikets = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    categories = orm.relation("Category", secondary="association", backref="news")
