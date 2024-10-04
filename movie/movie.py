from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r
from constants import HOST, MOVIE_PORT

app = Flask(__name__)

# Intégration des types déclarés dans le schéma GraphQL.
type_defs = load_schema_from_path('movie.graphql')

# Création des objets associés au schéma.
query = QueryType()
mutation = MutationType()
movie = ObjectType('Movie')
actor = ObjectType('Actor')

# Association du resolver à la requête associée dans le schéma.
query.set_field('movie_with_id', r.movie_with_id)
mutation.set_field('update_movie_rate', r.update_movie_rate)
movie.set_field('actors', r.resolve_actors_in_movie)

# Création du schéma dit exécutable avec les éléments précédents.
schema = make_executable_schema(type_defs, movie, query, mutation, actor)


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
