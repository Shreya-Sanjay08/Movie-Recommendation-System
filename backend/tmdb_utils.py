import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def search_movie(movie_title):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        return data['results'][0]  # return first match
    return None

def get_poster_url(movie):
    poster_path = movie.get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

def get_overview(movie):
    return movie.get("overview", "No overview available.")

def get_top_popular_movies(n=10):
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    return response.json().get("results", [])[:n]
