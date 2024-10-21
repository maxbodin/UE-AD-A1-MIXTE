# REST API
import json
import requests
from flask import Flask, request, jsonify, make_response

# CALLING gRPC requests
# import grpc
# from concurrent import futures
# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc


app = Flask(__name__)

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>", 200)


@app.route("/users", methods=['GET'])
def get_users():
    return jsonify(users), 200


@app.route("/users/<id_or_name>", methods=['GET'])
def get_user(id_or_name):
    for user in users:
        if user['id'] == id_or_name or user['name'].lower() == id_or_name.lower():
            return make_response(jsonify(user), 200)
    return jsonify({"error": "User not found"}), 404


@app.route("/adduser/<userid>", methods=['POST'])
def add_user(userid):
    req = request.get_json()

    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User ID already exists"}), 409)

    users.append(req)
    write(users)
    res = make_response(jsonify({"message": "User added"}), 200)
    return res


def write(all_users):
    with open('{}/data/users.json'.format("."), 'w') as f:
        movies_dict = {'users': all_users}
        json.dump(movies_dict, f)


@app.route("/userssetlastactive/<userid>", methods=['PUT'])
def update_user_last_active(userid):
    new_last_active = request.args.get('last_active', None)
    if not new_last_active:
        return jsonify({"error": "last_active not provided"}), 400

    for user in users:
        if str(user["id"]) == str(userid):
            user["last_active"] = new_last_active
            write(users)
            res = make_response(jsonify(user), 200)
            return res

    res = make_response(jsonify({"error": "User ID not found"}), 201)
    return res


@app.route("/users/<userid>", methods=['DELETE'])
def del_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            write(users)
            return make_response(jsonify(user), 200)

    res = make_response(jsonify({"error": "User ID not found"}), 400)
    return res


@app.route("/users/<userid>/bookings", methods=['GET'])
def get_user_bookings(userid):
    selected_user = None
    for user in users:
        if user['id'] == userid:
            selected_user = user
            break

    if not selected_user:
        return jsonify({"error": "User not found"}), 404

    user_id = selected_user['id']
    booking_service_url = f'http://{HOST}:{BOOKING_PORT}/bookings/{user_id}'

    try:
        response = requests.get(booking_service_url)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Bookings not found for the user"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Booking service is unavailable", "details": str(e)}), 500


@app.route("/users/<userid>/movies", methods=['GET'])
def get_user_movie_details(userid):
    selected_user = None
    for user in users:
        if user['id'] == userid:
            selected_user = user
            break

    if not selected_user:
        return jsonify({"error": "User not found"}), 404

    user_id = selected_user['id']

    # Fetch bookings from Booking service.
    try:
        booking_response = requests.get(f'http://{HOST}:{BOOKING_PORT}/bookings/{user_id}')
        if booking_response.status_code != 200:
            return jsonify({"error": "No bookings found for the user"}), 404

        bookings = booking_response.json()

        # Fetch movie details for each movie in the bookings.
        movie_details = []
        for booking in bookings:
            for date_entry in booking['dates']:
                for movie_id in date_entry['movies']:
                    # Define the GraphQL query and inject the movie_id.
                    graphql_query = {
                        'query': f"""
                            query {{
                                movie_with_id(_id: "{movie_id}") {{
                                    title
                                    rating
                                    director
                                }}
                            }}
                            """
                    }

                    # Make the POST request to the GraphQL endpoint.
                    movie_response = requests.post(f'http://{HOST}:{MOVIE_PORT}/graphql', json=graphql_query)

                    # Process the response.
                    if movie_response.status_code == 200:
                        movie_data = movie_response.json()
                        print(movie_data)
                        # Extract the movie data from the GraphQL response if available.
                        if "data" in movie_data and "movie_with_id" in movie_data["data"]:
                            movie_details.append(movie_data["data"]["movie_with_id"])

        if not movie_details:
            return jsonify({"error": "No movies found for the user's bookings"}), 404

        return jsonify(movie_details), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Booking or Movie service is unavailable", "details": str(e)}), 500


@app.route("/help", methods=['GET'])
def movie_help():
    endpoints = {
        "GET /": "Home page of the User service",
        "GET /users": "Get all the users",
        "GET /users/<id_or_name>": "Get a user by its ID or name",
        "POST /adduser/<userid>": "Add a new user (POST)",
        "PUT /userssetlastactive/<userid>": "Update user last active timestamp (PUT)",
        "DELETE /users/<userid>": "Delete a user by its ID (DELETE)",
        "GET /users/<userid>/bookings": "Get bookings for a specific user by their ID",
        "GET /users/<userid>/movies": "Get movie details for user's bookings"
    }
    return jsonify(endpoints), 200


if __name__ == "__main__":
    print("Server running in port %s" % 3004)
    app.run(host="0.0.0.0", port=3004)
