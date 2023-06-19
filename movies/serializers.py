from rest_framework import serializers

from movies.models import Movie, MovieOrder, Ratings


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    duration = serializers.CharField(allow_null=True, default=None)
    rating = serializers.ChoiceField(
        allow_null=True, choices=Ratings.choices, default=Ratings.G
    )
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.CharField(read_only=True, source="user.email")

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.SerializerMethodField(allow_null=True, read_only=True, source="movie.title")
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = serializers.DateTimeField(allow_null=True, read_only=True)
    buyed_by = serializers.SerializerMethodField(read_only=True, source="user.email")

    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)