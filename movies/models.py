from django.db import models
from django.contrib.auth import get_user_model


class Ratings(models.TextChoices):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


class Movie(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="movies",null=True)
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, blank=True, null=True)
    rating = models.CharField(max_length=20, choices=Ratings.choices, default=Ratings.G)
    synopsis = models.TextField(blank=True, null=True)

class MovieOrder(models.Model):
    movie = models.ForeignKey(
        "movies.Movie",on_delete=models.PROTECT, related_name="movie_order",
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="user_movie_order",
    )
    buyed_at = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return self.title
