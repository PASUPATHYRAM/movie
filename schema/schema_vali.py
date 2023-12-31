from pydantic import BaseModel,field_validator,ValidationError,Field
from typing import Optional
from datetime import datetime



def helper_year(year:int):
    if not year<=datetime.now().year and year>1900:
        raise ValueError("Please provide correct year")
    return year


class Movie_vali(BaseModel):
    # id: int
    name: str
    year: int
    director: str='Not Available'
    songs: bool

    @field_validator('year')
    def year_check(cls,v:int):
        try:
            return helper_year(v)
        except ValueError as exc:
            raise ValueError(f"Validation error for 'year': {str(exc)}") from exc

    @field_validator('name')
    def name_convert(cls,v:str):
        return v.title()

class Movieout(Movie_vali):
    id: int
    class Config:
        orm_mode=True

class Theatres_vali(BaseModel):

    theatre: str= Field(...)


    @field_validator('theatre')
    def name_convert1(cls, v: str):
        return v.upper()

class Theatres_out(Theatres_vali):
    id: int
    class Config:
        orm_mode=True







# a=Movie_vali(id=1,name='dere',year=2014,director='kbdn',songs=False)
# print(a.model_dump())

