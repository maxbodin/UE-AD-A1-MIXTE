from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r

MOVIE_PORT = 3001
HOST = '0.0.0.0'

app = Flask(__name__)

# LOAD TYPES
type_defs = load_schema_from_path('movie.graphql')

# CREATE TYPES
query = QueryType()
movie = ObjectType('Movie')

# RESOLVER -> MOVIES
query.set_field('movies', r.movies)
query.set_field('movie_with_id', r.movie_with_id)
query.set_field('movies_with_director', r.movies_with_director)
query.set_field('movie_with_title_exact', r.movie_with_title_exact)
query.set_field('movies_above_rating', r.movies_above_rating)
query.set_field('movies_with_actor', r.movies_with_actor)
query.set_field('top_movies_by_director', r.top_movies_by_director)

# RESOLVER -> ACTORS
query.set_field('actor_by_id', r.actor_by_id)
query.set_field('actor_film_count', r.actor_film_count)
query.set_field('actors_by_lastname', r.actors_by_lastname)
query.set_field('actors_in_movie', r.actors_in_movie)


# Création du schéma dit exécutable avec les éléments précédents.
schema = make_executable_schema(type_defs, movie, query)


@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# Graphql entry points
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    print("Server running in port %s" % MOVIE_PORT)
    app.run(host=HOST, port=MOVIE_PORT)
