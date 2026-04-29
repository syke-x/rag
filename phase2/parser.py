from models import MovieModel , GenreModel , StudioModel , PersonModel , ActingCreditModel
from typing import List , Optional 
import json 

def parse_tmdb_row(movie_row : dict , credit_rw : dict ) -> MovieModel : 

    def safe_json(value):
        if not value :
            return []
        if isinstance(value , list):
            return value 
        return json.loads(value)

    
    genres = safe_json(movie_row.get('genres' , []))
    production_companies = safe_json(movie_row.get('production_companies' , []))
    crew = safe_json(credit_rw.get('crew' , []))
    cast = safe_json(credit_rw.get('cast' , []))  

    release_date = movie_row.get('release_date')
    release_year = None 
    if release_date and isinstance(release_date , str) :
        try : 
            release_year = datetime.strptime(release_date, "%Y-%m-%d").year
        except ValueError:
            release_year = None

    directors = [ member["name"] for member in crew if member.get('job') == 'Director']

    top_cast = [
        actor["name"] for actor in cast if actor.get("billing_order" , 99) <= 10
    ]

    return MovieModel(
        movie_id = movie_row.get("id"),
        title = movie_row.get("title"),
        release_year,
        runtime = movie_row.get("runtime"),
        tagline = movie_row.get("tagline"),
        vote_average = movie_row.get("vote_average"),
        genres,
        studios
    )

