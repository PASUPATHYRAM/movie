from fastapi import APIRouter,Depends,Path,Body
from typing import List,Union,Dict,Tuple
from sqlalchemy.orm import Session
from exno1.service.services_layer import getting_all_movies,add_movie,modify_director,get_movie_by_year,\
    list_movie,movie_and_year,add_movie_theare,list_theatres,checktheatrenames,mo_the,del_all
from exno1.db_connection.database import db_conn
from exno1.schema.schema_vali import Movie_vali,Movieout,Theatres_vali
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

@router.get('/listmv',response_model=List[str])
def movie_list(db: Session=Depends(db_conn)):
    rsult=list_movie(db)
    return rsult

@router.get('/myear',response_model=List[Dict[int,List[str]]])
def movie_year(db: Session=Depends(db_conn)):
    rslt=movie_and_year(db)
    return rslt

# @router.post('/addmoviethetre',response_model=Dict[str,str])
# def mtheatre(db : Session=Depends(db_conn),movie_data=Movie_vali,theatre_data=Theatres_vali):
#     data1=add_movie_theare(db,movie_data,theatre_data)
#     return data1

@router.post('/addmoviethetre', response_model=Tuple[Movie_vali, Theatres_vali])
def mtheatre(db: Session = Depends(db_conn), movie_data: Movie_vali = Body(...), theatre_data: Theatres_vali = Body(...)):
    movie_db, theatre_db = add_movie_theare(db, movie_data, theatre_data)
    return movie_db, theatre_db

@router.get('/theatre',response_model=Dict[str,List[str]])
def movie_year(db: Session=Depends(db_conn)):
    rslt=list_theatres(db)
    return rslt

@router.get('/update',response_model=List[Tuple[str]])
def theateup(db: Session=Depends(db_conn)):
    up=checktheatrenames(db)
    return up

@router.get('/mvoie/{moviename}',response_model=List[Dict[str,str]])
def get_movie_name(db: Session=Depends(db_conn),moviename: str=Path(...)):
    result=mo_the(db,moviename)
    return result

@router.delete('/deleteall',response_model=Dict[str,str])
def del_records(db:Session=Depends(db_conn)):
    dele=del_all(db)
    return dele