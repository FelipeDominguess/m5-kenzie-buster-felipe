from . import views
from django.urls import path


urlpatterns = [
    path("movies/", views.MovieView.as_view()),
    path("movies/<int:movie_id>/", views.MovieDetailView.as_view()),
    path("movies/<int:movie_id>/orders/", views.MovieOrderView.as_view()),
]