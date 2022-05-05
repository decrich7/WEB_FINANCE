import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Portfel(SqlAlchemyBase):
    __tablename__ = 'portfel'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    yield_persent = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    volatility_stoks = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    horiz = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    short = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("news.id"))
    # user = orm.relation('News')
    # categories = orm.relation("Category", secondary="association", backref="portfel")
