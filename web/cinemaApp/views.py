import json
import time
import sys
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse

from cinemaApp.clients.graphql_service import call_graphql_service
from cinemaApp.clients.rest_service import call_rest_service
from cinemaApp.clients.grpc_service import call_grpc_service


def index(request):
    search_result = ""
    return render(request, 'cinemaApp/home.html')

# USERS
def list_users_view(request):
    all_users = call_rest_service(3004, 'users', 'GET')
    search_result = ""
    
    if request.method == 'POST':
        # Récupérer le terme de recherche soumis
        search_query = request.POST.get('search_query', '').strip()

        if search_query:
            # Filtrer les utilisateurs par le terme de recherche
            # On suppose ici que l'API REST supporte la recherche d'utilisateurs via une requête GET avec un paramètre de recherche
            search_result = call_rest_service(3004, f'users/{search_query}', 'GET')

            # Si l'API retourne une erreur
            if isinstance(search_result, dict) and search_result.get('error'):
                return render(request, 'cinemaApp/users_dashboard.html', {
                    'users': all_users,
                    'error': search_result['error'],
                    'search_result': None
                })

    # Afficher tous les utilisateurs au chargement initial ou les résultats de la recherche
    return render(request, 'cinemaApp/users_dashboard.html', {
        'users': all_users,
        'search_result': search_result
    })

def user_detail_view(request, id):
    user = call_rest_service(3004, f'users/{id}', 'GET')
    print("BOOKINGS")
    bookings = call_grpc_service('localhost:3002', 'GetBookingsOfUser', userId=id)
    for booking in bookings:
        booking['date'] = time.strftime('%d %B %Y', time.localtime(int(booking['date'])))
        for movie in booking['movies']:
            movie['movie'] = call_graphql_service(3001, f"{{ movie_with_id(_id: \"{movie['movieId']}\") {{ title }} }}").json()['data']['movie_with_id']['title']
    return render(request, 'cinemaApp/user.html', {'user': user, 'bookings': bookings})

def delete_user_view(request, id):
    # Make a DELETE request to the REST service to delete the user
    response = call_rest_service(3004, f'users/{id}', 'DELETE')
    
    # Handle cases where there is an error
    if isinstance(response, dict) and response.get('error'):
        # If there is an error, render the user_detail template with the error
        return render(request, 'cinemaApp/user.html', {'user': {'id': id}, 'error': response['error']})
    
    # Redirect to the users list page after successful deletion
    return redirect('users_list')

def add_user_view(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        
        if not name:
            return render(request, 'cinemaApp/add_user.html', {'error': "name should be defined"})
        
        newId = name.lower().replace(' ', '_')
        
        # Make a POST request to add the user
        response = call_rest_service(3004, 'adduser/{newId}', 'POST', data={'id':newId, 'name': name, 'last_active': time.time()})
        
        # Check if the user was successfully created
        if response.get('error'):
            return render(request, 'cinemaApp/add_user.html', {'error': response})
        
        # Redirect to the users list page after successful addition
        return redirect('users_list')

    # If GET request, render the form template
    return render(request, 'cinemaApp/add_user.html')

# MOVIES
def list_movies_view(request): 
    request_body = """
        {
            movies {
                id
                title
            }
        }
    """
    all_movies = call_graphql_service(port=3001, query=request_body).json()
    
    search_result = []
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '').strip()
        
        if search_query:
            request_body = f"""
                {{
                    movies_with_title_contains(title: "{search_query}") {{
                        id
                        title
                    }}
                }}
            """
            search_result = call_graphql_service(port=3001, query=request_body).json()
            
            # Check for errors in response
            if isinstance(search_result, dict) and search_result.get('errors'):
                return render(request, 'cinemaApp/users_dashboard.html', {
                    'movies': all_movies['data']['movies'],
                    'error': search_result['errors'],
                    'search_result': []
                })
            search_result = search_result.get('data', {}).get('movies_with_title_contains', [])

    return render(request, 'cinemaApp/movies.html', {
        'movies': all_movies['data']['movies'],
        'search_result': search_result
    })

def movie_detail_view(request, id):
    request_body = f"""
        {{
            movie_with_id(_id: "{id}") {{
                id
                title
                director
                rating
            }}
        }}
    """
    movie = call_graphql_service(port=3001, query=request_body)
    movie = movie.json()
    
    request_body = f"""
        {{
            actors_in_movie(movie_id: "{id}") {{
                id
                firstname
                lastname
                birth_year
            }}
        }}
    """
    actors = call_graphql_service(port=3001, query=request_body)
    actors = actors.json()
    
    return render(request, 'cinemaApp/movie.html', {'movie': movie['data']['movie_with_id'], 'actors': actors['data']['actors_in_movie']})

def add_movie_view(request):
    all_actors = call_graphql_service(port=3001, query="{ actors { id firstname lastname } }").json()
    if request.method == 'POST':
        
        # ADD MOVIE
        title = request.POST.get('title')
        director = request.POST.get('director')
        rating = 5
        actors = request.POST.getlist('actors')
        actors_json = json.dumps(actors)  
        
        if not title or not director:
            return render(request, 'cinemaApp/add_movie.html', {'error': "All fields should be defined"})
        
        if not actors:
            return render(request, 'cinemaApp/add_movie.html', {'error': "At least one actor must be selected"})

        
        newId = uuid.uuid4()
        
        request_body = f"""
            mutation {{
                add_movie(_id: "{newId}", title: "{title}", director: "{director}", rating: {rating}, actors: {actors_json}) {{
                    id
                    title
                    director
                    rating
                    actors {{
                        id
                    }}
                }}
            }}
        """
        response = call_graphql_service(port=3001, query=request_body)
        response = response.json()
        
        if response.get('errors'):
            return render(request, 'cinemaApp/add_movie.html', {'error': response['errors']})
        
        
        return redirect('movies_list')
    
    return render(request, 'cinemaApp/add_movie.html', {'actors': all_actors['data']['actors']})

def delete_movie_view(request, id):
    query = f"""
        mutation {{
            delete_movie(_id: "{id}") {{
                id
            }}
        }}
    """
    response = call_graphql_service(port=3001, query=query)
    response = response.json()
    
    if response.get('errors'):
        return render(request, 'cinemaApp/movie.html', {'movie': {'id': id}, 'error': response['errors']})
    
    return redirect('movies_list')

# ACTORS$
def list_actors_view(request):
    request_body = """
        {
            actors {
                id
                firstname
                lastname
                birth_year
            }
        }
    """
    actors = call_graphql_service(port=3001, query=request_body)
    actors = actors.json()
    
    return render(request, 'cinemaApp/actors.html', {'actors': actors['data']['actors']})

def actor_detail_view(request, id):
    request_body = f"""
        {{
            actor_with_id(_id: "{id}") {{
                id
                firstname
                lastname
                birth_year
            }}
        }}
    """
    actor = call_graphql_service(port=3001, query=request_body)
    actor = actor.json()
    
    request_body = f"""
        {{
            actor_film_count(_id: "{id}")
        }}
    """
    film_count = call_graphql_service(port=3001, query=request_body)
    film_count = film_count.json()
    
    request_body = f"""
        {{
            movies_with_actor(actor_id: "{id}") {{
                id
                title
            }}
        }}
    """
    
    movies = call_graphql_service(port=3001, query=request_body)
    movies = movies.json()
    
    return render(request, 'cinemaApp/actor.html', {
        'actor': actor['data']['actor_with_id'], 
        'film_count': film_count, 
        'movies': movies['data']['movies_with_actor']
    })

# SHOWTIMES
def showtimes_view(request):
    request_body = """
        {
            showtimes {
                id
                date
                movies {
                    id
                    title
                }
            }
        }
    """
    showtimes = call_graphql_service(port=3002, query=request_body)
    showtimes = showtimes.json()
    
    return render(request, 'cinemaApp/showtimes.html', {'showtimes': showtimes['data']['showtimes']})
