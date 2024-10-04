import json


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def actor_with_id(_, info, _id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor


def update_movie_rate(_, info, _id, _rate):
    new_movies = {}
    new_movie = {}
    with open('{}/data/movies.json'.format("."), "r") as read_file:
        movies = json.load(read_file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                new_movie = movie
                new_movies = movies
    with open('{}/data/movies.json'.format("."), "w") as write_file:
        json.dump(new_movies, write_file)
    return new_movie


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result
