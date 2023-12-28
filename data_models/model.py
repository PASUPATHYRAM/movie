from sqlalchemy import Column,String,Integer,Boolean
from ..db_connection.database import Base

class Movie(Base):
    __tablename__="movies"

    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    year=Column(Integer)
    director=Column(String)
    songs=Column(Boolean)