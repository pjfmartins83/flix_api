from rest_framework import serializers
from movies.models import Movie


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"

    def validate_release_date(self, value):
        if value.year < 1990:
            raise serializers.ValidationError(
                "A data de lançamento não pode ser anterior a 1990."
            )
        return value

    def validate_synopsis(self, value):
        if len(value) > 200:
            raise serializers.ValidationError(
                "Sinopse não deve ter mais que 200 caracteres!"
            )
        return value
