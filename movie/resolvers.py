import json


def movies(_, info):
    allMovies = []
    with open("./data/movies.json", "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            allMovies.append(movie)
    return allMovies

def movie_with_id(_, info, _id):
    with open('./data/movies.json', "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie
    return None

def movies_with_director(_, info, director):
    movies_array = []
    with open("./data/movies.json", "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie["director"] == director:
                movies_array.append(movie)
    return movies_array

def movies_above_rating(_, info, rating):
    movies_array = []
    with open("./data/movies.json", "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie["rating"] >= rating:
                movies_array.append(movie)
    return movies_array

def movie_with_title_exact(_, info, title):
    with open('./data/movies.json', "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == title:
                return movie
    return None

def movie_with_title_contains(_, info, title):
    movies_array = []
    with open('./data/movies.json', "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if title.lower() in movie["title"].lower():
                movies_array.append(movie)
    return movies_array

def movies_with_actor(_, info, actor_id):
    with open("./data/actors.json", "r") as actors_file:
        actors = json.load(actors_file)
        actor_films = []
        for actor in actors.get("actors", []):
            if actor["id"] == actor_id:
                actor_films = actor.get("films", [])
                break

    if not actor_films:
        return []

    movies_array = []
    with open("./data/movies.json", "r") as movies_file:
        movies = json.load(movies_file)
        for movie in movies.get("movies", []):
            if movie["id"] in actor_films:
                movies_array.append(movie)

    return movies_array

def top_movies_by_director(_, info, director, count):
    with open("./data/movies.json", "r") as file:
        movies = json.load(file)
        director_movies = [
            movie for movie in movies["movies"] if movie["director"].lower() == director.lower()
        ]
        sorted_movies = sorted(director_movies, key=lambda x: x["rating"], reverse=True)
    return sorted_movies[:count]



def actor_by_id(_, info, _id):
    with open("./data/actors.json", "r") as file:
        actors = json.load(file)
        for actor in actors.get("actors", []):
            if actor["id"] == _id:
                return actor

def actor_film_count(_, info, id):
    with open("./data/actors.json", "r") as file:
        actors = json.load(file)
        for actor in actors.get("actors", []):
            if actor["id"] == id:
                return len(actor.get("films", []))
    return 0

def actors_by_lastname(_, info, lastname):
    actorsArray = []
    with open("./data/actors.json", "r") as file:
        actors = json.load(file)
        for actor in actors.get("actors", []):
            if actor["lastname"].lower() == lastname.lower():
                actorsArray.append(actor)
    return actorsArray

def actors_in_movie(_, info, movie_id):
    with open("./data/movies.json", "r") as movie_file:
        movies = json.load(movie_file)
        movie_actors = []
        for movie in movies.get("movies", []):
            if movie["title"].lower() == movie_id.lower():
                movie_actors = movie.get("actors", [])
                break

    actorsArray = []
    if movie_actors:
        with open("./data/actors.json", "r") as actor_file:
            actors = json.load(actor_file)
            for actor in actors.get("actors", []):
                if actor["id"] in movie_actors:
                    actorsArray.append(actor)

    return actorsArray
