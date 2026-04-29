from pydantic import BaseModel 
from typing import List , Optional

class GenereModel(BaseModel) :
    genre_id : int 
    name : str 

class StudioModel(BaseModel) :
    studio_id : int 
    name : str 
    country : Optional[str] = None 

class PersonModel(BaseModel):
    person_id : int
    name : str 
    birth_year : Optional[int] = None 

class ActingCreditModel(BaseModel):
    person_id :int 
    role : str
    billing_order : int 

class MovieModel(BaseModel):
    movie_id : int 
    title : str
    release_year : Optional[int] = None 
    runtime : Optional[int] = None 
    overview : str 
    tagline : Optional[str] = None 
    vote_average : float 
    genres : List[GenereModel]
    studios : List[StudioModel]
    directors : List[PersonModel]
    cast : List[ActingCreditModel] 