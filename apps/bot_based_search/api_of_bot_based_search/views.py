# views.py
from rest_framework import generics

# filtering
from django_filters.rest_framework import DjangoFilterBackend
from .filters_backend import MovieFilter

# searching 
from rest_framework import filters

# serializers 
from .serializers import  ( 
    MovieTitleSerializer, 
    LightCastSerializer, 
    LightCreatorSerializer, 
    LightWriterSerializer
)


#models 
from app6_movie.models import Movie, UserMovieWatchlist
from app3_cast.models import Cast
from app4_creator.models import Creator
from app5_writer.models import Writer

# pagination
from shared.pagination import GlobalPagination as Global


#datetime 
from datetime import timedelta
from django.utils import timezone





# searching based on these stuffs 
class TitleList(generics.ListAPIView):
    ''' all movies based on title '''
    serializer_class = MovieTitleSerializer  # Assuming you have a serializer for Movie
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'moviemedia__name', 
    ]
    pagination_class = Global

    def get_queryset(self):
        return Movie.objects.only(
            'id',
            'moviemedia__name',
            'movie_general_detail__duration',
            'movie_general_detail__avg_rating',
            'movie_general_detail__storyline',
            'movie_general_detail__duration',
            'movie_core_detail__release_date',
            'movie_core_detail__also_known_as'
        ).select_related(
            'movie_general_detail',
            'movie_core_detail',
            'moviemedia'
        ).prefetch_related(
            'moviemedia__media_files'
        )



class CastList(generics.ListAPIView):
    ''' all movies based on cast '''
    serializer_class = LightCastSerializer  # Assuming you have a serializer for Cast
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'castmedia__name',
    ]
    # pagination_class = Global

    def get_queryset(self):
        return Cast.objects.select_related(
            'castmedia'
        ).prefetch_related(
            'castmedia__media_files',
            'core_detail',
        )


class CreatorList(generics.ListAPIView):
    serializer_class = LightCreatorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'creatormedia__name',
    ]

    def get_queryset(self):
        return Creator.objects.select_related(
            'creatormedia'
        ).prefetch_related(
            'creatormedia__media_files',
            'creator_core_detail',
        )


class WriterList(generics.ListAPIView):
    serializer_class = LightWriterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'writermedia__name'
    ]

    def get_queryset(self):
        return Writer.objects.select_related(
            'writermedia'
        ).prefetch_related(
            'writermedia__media_files',
            'writer_core_detail'
        )
    


# filtering [predefined tags]
class BasedOn_Movie_Cast(generics.ListAPIView):
    serializer_class = MovieTitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie_cast']  # Filtering by Cast ID

    def get_queryset(self):
        return Movie.objects.only(
            'id',
            'moviemedia__name',
            'movie_general_detail__avg_rating',
            'movie_general_detail__duration',
            'movie_general_detail__storyline',
            'movie_core_detail__release_date',
            'movie_core_detail__also_known_as'
        ).select_related(
            'moviemedia',
            'movie_general_detail',
            'movie_core_detail',
        ).prefetch_related(
            'moviemedia__media_files',
            'movie_cast__castmedia__media_files',
        ).distinct()


class BasedOn_Movie_Ratings(generics.ListAPIView):
    serializer_class = MovieTitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter  #  changed from filterset_fields to filterset_class

    def get_queryset(self):
        qs =  Movie.objects.only(
            'id',
            'moviemedia__name',
            'movie_general_detail__avg_rating',
            'movie_general_detail__duration',
            'movie_general_detail__storyline',
            'movie_core_detail__release_date',
            'movie_core_detail__also_known_as'
        ).select_related(
            'moviemedia',
            'movie_general_detail',
            'movie_core_detail',
        ).prefetch_related(
            'moviemedia__media_files',
            'movie_cast__castmedia__media_files',
        ).order_by('-movie_general_detail__avg_rating').distinct()

        return qs


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['watchlisted_ids'] = getattr(self, 'watchlisted_movie_ids', set())
        return context


class BasedOn_Movie_Genre(generics.ListAPIView):
    serializer_class = MovieTitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie_genre']  

    def get_queryset(self):
        return Movie.objects.select_related(
            'moviemedia',
            'movie_general_detail',
            'movie_core_detail'
        ).prefetch_related(
            'moviemedia__media_files',
            'movie_genre'
        ).only(
            'id',
            'moviemedia__name',
            'movie_general_detail__avg_rating',
            'movie_general_detail__duration',
            'movie_general_detail__storyline',
            'movie_core_detail__release_date',
            'movie_core_detail__also_known_as'
        )



class BasedOn_TvShow_Cast(generics.ListAPIView):
    pass 

class BasedOn_TvShow_Ratings(generics.ListAPIView):
    pass 

class BasedOn_Episode_Ratings(generics.ListAPIView):
    pass 



class BasedOn_TvShow_Genre(generics.ListAPIView):
    pass 

class BasedOn_Movie_Country(generics.ListAPIView):
    pass 

class BasedOn_TvShow_Country(generics.ListAPIView):
    pass 

class BasedOn_TvShow_InTheaters(generics.ListAPIView):
    pass 

class BasedOn_Movie_InTheaters(generics.ListAPIView):
    pass 

class BasedOn_TvShow_InTheaters(generics.ListAPIView):
    pass 








# Ordering 
class TvShow_Rating(generics.ListAPIView):
    pass 

class Movie_Rating(generics.ListAPIView):
    pass 

class Episode_Rating(generics.ListAPIView):
    pass 


class Movie_ReleaseDate(generics.ListAPIView):
    pass 

class TvShow_ReleaseDate(generics.ListAPIView):
    pass 

class Episode_ReleaseDate(generics.ListAPIView):
    pass









# class BasedOn_Movie_InTheaters(generics.ListAPIView):
#     today = timezone.now().date()
#     thirty_days_ago = today - timedelta(days=30)
#     serializer_class = MovieTitleSerializer
#     queryset = Movie.objects.select_related(
#                 'moviemedia',
#                 'movie_general_detail',
#                 'movie_core_detail',
#             ).prefetch_related(
#                 'movie_genre',
#                 'moviemedia__media_files',
#             ).only(
#                 'id',
#                 'moviemedia__name',
#                 'movie_general_detail__avg_rating',
#                 'movie_general_detail__duration',
#                 'movie_general_detail__storyline',
#                 'movie_core_detail__release_date',
#                 'movie_core_detail__also_known_as',
#             ).filter(
#                 movie_core_detail__release_date__gte=thirty_days_ago,
#                 movie_core_detail__release_date__lte=today
#             ).order_by('-movie_core_detail__release_date')

