from django.urls import path
from django.http import HttpResponseRedirect

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users", views.list_users_view, name="users_list"),
    path("users/<str:id>", views.user_detail_view, name="user_detail"),
    path('users/add/', views.add_user_view, name='add_user'),
    path('users/delete/<str:id>', views.delete_user_view, name='delete_user'),
    
    path("movies", views.list_movies_view, name="movies_list"),
    path("movies/<str:id>", views.movie_detail_view, name="movie_detail"),
    path('movies/add/', views.add_movie_view, name='add_movie'),
    path('movies/delete/<str:id>', views.delete_movie_view, name='delete_movie'),
    
    path("actors", views.list_actors_view, name="actors_list"),
    path("actors/<str:id>", views.actor_detail_view, name="actor_detail"),
    path("actors/add/", views.add_actor_view, name="add_actor"),
    path("actors/delete/<str:id>", views.delete_actor_view, name="delete_actor"),
    
    path("showtimes", views.showtimes_view, name="showtimes_list"),
]   