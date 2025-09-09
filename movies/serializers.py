from django.db.models import Avg
from rest_framework import serializers
from movies.models import Movie
from genres.serializers import GenreSerializer
from actors.serializers import ActorSerializer


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"

    def validate_release_date(self, value):
        if value.year < 1900:
            raise serializers.ValidationError(
                "A data de lançamento não pode ser anterior a 1900."
            )
        return value

    def validate_synopsis(self, value):
        if len(value) > 500:
            raise serializers.ValidationError(
                "Sinopse não deve ter mais que 500 caracteres!"
            )
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    cast = ActorSerializer(many=True)
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "genre", "cast", "release_date", "rate", "synopsis"]

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg("stars"))["stars__avg"]

        if rate:
            return rate
        return None
