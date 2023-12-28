from fastapi import APIRouter,Depends,Path,Body
from typing import List,Union
from sqlalchemy.orm import Session
from exno1.service.services_layer import getting_all_movies,add_movie,modify_director,get_movie_by_year
from exno1.db_connection.database import db_conn
from exno1.schema.schema_vali import Movie_vali,Movieout
router=APIRouter()



@router.get('/movies',response_model=List[Movieout])
def get_movies(db:Session=Depends(db_conn)):
    movies=getting_all_movies(db)
    return movies

@router.post('/add',response_model=Movie_vali)
def create_movie(movie_data: Movie_vali,db:Session = Depends(db_conn)):
    movies=add_movie(db,movie_data)
    return movies

@router.patch('/modify/{mname}',response_model=Union[Movie_vali,str])
def modify_data(db: Session=Depends(db_conn),mname: str=Path(...),direct: str=Body(...)):
    data_fetch=modify_director(db,mname)
    if not data_fetch:
        return "Movie not found"
    data_fetch.director= direct
    db.add(data_fetch)
    db.commit()
    return "Successfullu changed"

@router.get('/year/{Year}',response_model=Union[List[Movie_vali],str])
def movie_year_all(db:Session=Depends(db_conn),Year: int=Path(...)):
    return get_movie_by_year(db,Year)




