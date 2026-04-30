from pydantic import BaseModel , field_validator 
from typing import List , Optional

class GenreModel(BaseModel) :
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
    @field_validator("overview")
    @classmethod
    def overview_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("overview cannot be empty — required for embeddings")
        return v.strip() 

    @field_validator("runtime", mode="before")
    @classmethod
    def coerce_zero_runtime_to_none(cls, v):
        if v == 0:
            return None
        return v

    movie_id : int 
    title : str
    release_year : Optional[int] = None 
    runtime : Optional[int] = None 
    overview : str 
    tagline : Optional[str] = None 
    vote_average : float 
    genres : List[GenreModel]
    studios : List[StudioModel]
    directors : List[PersonModel]
    cast : List[ActingCreditModel] 