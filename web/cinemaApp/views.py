import time
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .clients.graphQL import call_graphql_service
from .clients.REST import call_rest_service



def index(request):
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
    bookings = call_rest_service(3004, f'bookings/{id}', 'GET')
    return render(request, 'cinemaApp/user.html', {'user': user})

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
                actors {{
                    id
                    firstname
                    lastname
                    birth_year
                    films
                }}
            }}
        }}
    """
    movie = call_graphql_service(port=3001, query=request_body)
    movie = movie.json()
    
    return render(request, 'cinemaApp/movie.html', {'movie': movie['data']['movie_with_id']})