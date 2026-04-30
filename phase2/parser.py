from models import MovieModel , GenreModel , StudioModel , PersonModel , ActingCreditModel
from typing import List , Optional 
import json 
from datetime import datetime

def parse_tmdb_row(raw_row : dict) -> MovieModel : 

    def safe_json(value):
        if not value :
            return []
        if isinstance(value , list):
            return value 
        return json.loads(value)

    
    genres_raw = safe_json(raw_row.get('genres', []))
    genres = [GenreModel(genre_id=g["id"], name=g["name"]) for g in genres_raw]
    production_companies = safe_json(raw_row.get('production_companies' , []))
    crew = safe_json(raw_row.get('crew' , []))
    cast = safe_json(raw_row.get('cast' , []))  

    release_date = raw_row.get('release_date')
    release_year = None 
    if release_date and isinstance(release_date , str) :
        try : 
            release_year = datetime.strptime(release_date, "%Y-%m-%d").year
        except ValueError:
            release_year = None

    directors = [
        PersonModel(person_id=member["id"] , name = member["name"])
        for member in crew 
        if member.get("job") == "Director"
    ]

    top_cast = [
        ActingCreditModel(
            person_id=actor["id"],
            role=actor.get("character" , "Unknown"),
            billing_order=actor["order"]
        )

        for actor in cast 
        if actor.get("order" , 99) < 10 
    ]

    studios = [
        StudioModel(studio_id=s["id"], name=s["name"])
        for s in production_companies
    ]


    return MovieModel(
        movie_id = raw_row.get("id"),
        title = raw_row.get("title_x") or raw_row.get("title"),
        release_year=release_year,
        runtime=raw_row.get("runtime") or None,
        overview=raw_row.get("overview", ""),
        tagline = raw_row.get("tagline"),
        vote_average = raw_row.get("vote_average"),
        genres=genres,
        studios=studios,
        directors=directors,
        cast=top_cast
    )



