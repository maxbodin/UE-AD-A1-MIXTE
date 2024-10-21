from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users", views.list_users_view, name="users_list"),
    path("users/<str:id>", views.user_detail_view, name="user_detail"),
    path('users/add/', views.add_user_view, name='add_user'),
    path('users/delete/<str:id>', views.delete_user_view, name='delete_user')
]