from sqlalchemy import Column,String,Integer,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from ..db_connection.database import Base

class Movie(Base):
    __tablename__="movies"

    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    year=Column(Integer)
    director=Column(String)
    songs=Column(Boolean)

    theatres_rel=relationship('Theatres',secondary='cross_ref',back_populates='movies_rel')


class Theatres(Base):
    __tablename__='theatres'
    id=Column(Integer,primary_key=True,autoincrement=True)
    theatre=Column(String)
    # movie_id=Column(Integer,ForeignKey('movies.id'))
    movies_rel=relationship('Movie',secondary='cross_ref',back_populates='theatres_rel')

class Cross_ref(Base):
    __tablename__='cross_ref'
    movie_id=Column(Integer,ForeignKey('movies.id'),primary_key=True)
    theatre_id=Column(Integer,ForeignKey('theatres.id'),primary_key=True)
