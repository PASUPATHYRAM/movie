from sqlalchemy.orm import Session
from exno1.schema.schema_vali import Movie_vali
from exno1.data_models.model import Movie,Theatres,Cross_ref
from exno1.schema.schema_vali import Movie_vali,Theatres_vali
from exno1.db_connection.database import db_conn
from collections import defaultdict

def getting_all_movies(db: Session):
    result=db.query(Movie).all()
    return result

def add_movie(db: Session,movie_data=Movie_vali):
    movie_dict = movie_data.model_dump()
    movie_dict.pop('id',None)
    movie = Movie(**movie_dict)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

def modify_director(db: Session,movie_name: str):
    name_filter=db.query(Movie).filter(Movie.name==movie_name).first()
    return name_filter

def get_movie_by_year(db: Session,year: int):
    year_filter=db.query(Movie).filter(Movie.year==year).all()
    return [Movie_vali.model_validate(movie.__dict__) for movie in year_filter]

def list_movie(db: Session):
    list_movies=db.query(Movie.name).all()
    return [names[0] for names in list_movies]

def movie_and_year(db: Session):
    m_y=db.query(Movie.name,Movie.year).all()
    result=defaultdict(list)
    for name,year in m_y:
        result[int(year)].append(name)
    return [dict(result)]


def add_movie_theare(db: Session,movie_data=Movie_vali,theater_data=Theatres_vali):
    movie_dict=movie_data.model_dump()
    movie_db=Movie(**movie_dict)
    db.add(movie_db)
    db.flush()  # Assign an ID to movie_db

    theater_dict = theater_data.model_dump()
    theatre_db = Theatres(**theater_dict)
    db.add(theatre_db)
    db.flush()  # Assign an ID to theatre_db

    new_cross_ref = Cross_ref(movie_id=movie_db.id, theatre_id=theatre_db.id)
    db.add(new_cross_ref)

    db.commit()

    db.refresh(movie_db)
    db.refresh(theatre_db)

    return movie_db, theatre_db

def list_theatres(db: Session):
    the_query=db.query(Theatres).all()
    t_set=set()

    for t in the_query:
        t_set.add(t.theatre)
    default_list = defaultdict(list)
    default_list['Theatres']=list(t_set)
    return default_list


def checktheatrenames(db: Session):
    ch=db.query(Theatres).all()
    for theatres in ch:
        if theatres.theatre != theatres.theatre.upper():
            theatres.theatre = theatres.theatre.upper()
    db.commit()
    return db.query(Theatres.theatre).all()

def mo_the(db: Session, mv: str):
    query = db.query(Movie).filter(Movie.name == mv).first()
    if query:
        print(f"Found movie: {query.name}")
        print(f"Found movie: {query.theatres_rel}")
        empty_list = []
        for thea in query.theatres_rel:
            print(f"Found theatre: {thea.theatre}")
            empty_list.append({'movie': query.name, 'theatre': thea.theatre})
        return empty_list
    print(f"No movie found with name: {mv}")
    return []

def del_all(db: Session):
    db.query(Movie).delete()
    db.query(Theatres).delete()
    db.query(Cross_ref).delete()
    db.commit()
    return {'message':'Successfully deleted'}
