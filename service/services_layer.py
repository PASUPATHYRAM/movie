from sqlalchemy.orm import Session
from ..schema.schema_vali import Movie_vali
from ..data_models.model import Movie
from exno1.schema.schema_vali import Movie_vali

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


