import pandas as pd 
from pydantic import ValidationError
from parser import parse_tmdb_row

def load_data(movies_path : str , credits_path : str) :

    movies_df = pd.read_csv(movies_path)
    credits_df = pd.read_csv(credits_path)

    merged_df = movies_df.merge(credits_df , left_on='id' , right_on='movie_id')

    total_rows = len(merged_df)

    parsed_movies = []
    failed_rows = []

    for index , row in merged_df.iterrows():

        row_dict = row.to_dict()

        row_dict = {k : (None if pd.isna(v) else v) for k , v in row_dict.items()}

        try : 
            movie_model = parse_tmdb_row(row_dict )
            parsed_movies.append(movie_model)

        except ValidationError as e :
            title = row_dict.get("title_x") or row_dict.get("title", "Unknown Title")
            error_reasons = [f"{err['loc'][0]} : {err['msg']}" for err in e.errors()]
            failed_rows.append({"title": title, "reasons": error_reasons})

        except Exception as e :
            title = row_dict.get('title_x') or row_dict.get('title', 'Unknown Title')
            failed_rows.append({"title": title, "reasons": [str(e)]})

    print("\n--- Ingestion Parsing Summary ---")
    print(f"Total rows processed : {total_rows}")
    print(f"Successfully parsed  : {len(parsed_movies)}")
    print(f"Failed to parse      : {len(failed_rows)}")

    if failed_rows:
        print("\n--- Top 5 Failure Reasons ---")
        for fail in failed_rows[:5]:
            print(f"- {fail['title']} -> {', '.join(fail['reasons'])}")
    return parsed_movies


if __name__ == "__main__" :
    movies_csv = "data/raw/tmdb_5000_movies.csv"
    credits_csv = "data/raw/tmdb_5000_credits.csv"

    movies = load_data(movies_csv , credits_csv)

