import json


# RESOLVER -> MOVIES
def movies(_, info):
    with open("./data/movies.json", "r") as file:
        all_movies = json.load(file)
    return all_movies["movies"]


def movie_with_id(_, info, _id):
    with open('./data/movies.json', "r") as file:
        all_movies = json.load(file)
        for movie in all_movies['movies']:
            if movie['id'] == _id:
                return movie


def movies_with_director(_, info, director):
    movies_array = []
    with open("./data/movies.json", "r") as file:
        all_movies = json.load(file)
        for movie in all_movies["movies"]:
            if movie["director"] == director:
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
        all_movies = json.load(movies_file)
        for movie in all_movies.get("movies", []):
            if movie["id"] in actor_films:
                movies_array.append(movie)

    return movies_array


def movies_above_rating(_, info, rating):
    movies_array = []
    with open("./data/movies.json", "r") as file:
        all_movies = json.load(file)
        for movie in all_movies["movies"]:
            if movie["rating"] >= rating:
                movies_array.append(movie)
    return movies_array


def movie_with_title_exact(_, info, title):
    with open('./data/movies.json', "r") as file:
        all_movies = json.load(file)
        for movie in all_movies['movies']:
            if movie['title'] == title:
                return movie
    return None


def movie_with_title_contains(_, info, title):
    movies_array = []
    with open('./data/movies.json', "r") as file:
        all_movies = json.load(file)
        for movie in all_movies['movies']:
            if title.lower() in movie["title"].lower():
                movies_array.append(movie)
    return movies_array


def top_movies_by_director(_, info, director, count):
    with open("./data/movies.json", "r") as file:
        all_movies = json.load(file)
        director_movies = [
            movie for movie in all_movies["movies"] if movie["director"].lower() == director.lower()
        ]
        sorted_movies = sorted(director_movies, key=lambda x: x["rating"], reverse=True)
    return sorted_movies[:count]


# RESOLVER -> ACTORS
def actors(_, info):
    with open("./data/actors.json", "r") as file:
        all_actors = json.load(file)
    return all_actors["actors"]


def actor_with_id(_, info, _id):
    with open('./data/actors.json', "r") as file:
        all_actors = json.load(file)
        for actor in all_actors['actors']:
            if actor['id'] == _id:
                return actor


def actor_film_count(_, info, _id):
    with open("./data/actors.json", "r") as file:
        all_actors = json.load(file)
        for actor in all_actors.get("actors", []):
            if actor["id"] == _id:
                return len(actor.get("films", []))
    return 0


def actors_by_lastname(_, info, lastname):
    selected_actors = []
    with open("./data/actors.json", "r") as file:
        all_actors = json.load(file)
        for actor in all_actors.get("actors", []):
            if actor["lastname"].lower() == lastname.lower():
                selected_actors.append(actor)
    return selected_actors


def actors_in_movie(_, info, movie_id):
    with open("./data/movies.json", "r") as movie_file:
        all_movies = json.load(movie_file)
        movie_actors = []
        for movie in all_movies.get("movies", []):
            if movie["title"].lower() == movie_id.lower():
                movie_actors = movie.get("actors", [])
                break

    selected_actors = []
    if movie_actors:
        with open("./data/actors.json", "r") as actor_file:
            all_actors = json.load(actor_file)
            for actor in all_actors.get("actors", []):
                if actor["id"] in movie_actors:
                    selected_actors.append(actor)

    return selected_actors


def update_movie_rate(_, info, _id, _rate):
    new_movies = {}
    new_movie = {}
    with open('./data/movies.json', "r") as read_file:
        all_movies = json.load(read_file)
        for movie in all_movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                new_movie = movie
                new_movies = all_movies
    with open('./data/movies.json', "w") as write_file:
        json.dump(new_movies, write_file)
    return new_movie
