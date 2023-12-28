from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATA_BASE_STRING='sqlite:///./db_connection/data.db'

engine=create_engine(url=DATA_BASE_STRING,connect_args={'check_same_thread':True})

connection=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base() # to create tables



def db_conn():
    orm_sess=connection()
    try:
        yield orm_sess
    finally:
        orm_sess.close()

def create_tables():

    from exno1.data_models.model import Movie
    Base.metadata.create_all(engine)

