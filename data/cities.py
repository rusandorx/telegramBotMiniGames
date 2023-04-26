import sqlalchemy

from .db_session import SqlAlchemyBase


class City(SqlAlchemyBase):
    __tablename__ = 'cities'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.String)
    population = sqlalchemy.Column(sqlalchemy.Integer)
