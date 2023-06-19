from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie
from movies.permissions import EmployeePermission, IsOwner
from movies.serializers import MovieOrderSerializer, MovieSerializer
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [EmployeePermission]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:

        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [EmployeePermission, IsOwner]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, EmployeePermission]

    def post(self, request: Request, movie_id: int) -> Response:

        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)