from django.urls import path
from .views import *


urlpatterns = [
    path('movies',allMovies,name="allMovies"),
    path('movies/recommend',recommendMovies,name="recommendMovies"),
    path('movies/favorites',favorites,name="favoritesApi"),
    path('movies/filter',filterView,name="filter"),
    path('movies/addToFav',addToFav,name="addToFavApi"),
    path('movies/removeFromFav',removeFromFav,name="removeFromFavApi"),
    path('movies/<str:movie_id>',movieView,name="movieApi"),
    path('user/history',history_view,name="historyApi"),
    path('user/login',login_view,name="loginApi"),
    path('user/register',signup,name="registerApi"),
    path('user/logout',logout,name="logoutApi"),
]
