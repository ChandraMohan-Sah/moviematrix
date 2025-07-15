from django_filters import rest_framework as custom_filters
from app6_movie.models import Movie

class MovieFilter(custom_filters.FilterSet):
    avg_rating = custom_filters.RangeFilter(field_name='movie_general_detail__avg_rating')

    class Meta:
        model = Movie
        fields = ['avg_rating']


