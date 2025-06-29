# serializers.py

from rest_framework import serializers 
from app1_media_manger.models import MediaFile, MovieMedia
from app6_movie.models import ( 
    Movie, MovieGeneralDetail , MovieCoreDetail , MovieBoxOffice, 
    MovieTechSpecs, MovieRatingReview, UserMovieWatchlist ,
    UserMovieViewed, MovieVotes, MovieWatchHistory
)
from app2_gener_platform.models import Genre, Platform
from app3_cast.models import Cast
from app4_creator.models import Creator
from app5_writer.models import Writer
from app8_lang_prod_company.models import Language, ProductionCompany

from django.contrib.auth import get_user_model
User = get_user_model()
 

'''
    Notes : (serializer )
        - Translator: between Python models and JSON
        - Gatekeeper: validates what's allowed in and what's shown outside
'''


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MediaFile 
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']
        ref_name = "app6-mediafilemanager"


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='moviemedia.name', read_only=True)
    banners = MediaFileSerializer(many=True, read_only=True)
    thumbnails = MediaFileSerializer(many=True, read_only=True)
    trailers = MediaFileSerializer(many=True, read_only=True)
    video = MediaFileSerializer(many=True, read_only=True)
    related_pic = MediaFileSerializer(many=True, read_only=True)

    moviemedia = serializers.SlugRelatedField(
        slug_field = 'movie_slug', # Match using `movie_slug` instead of ID
        queryset = MovieMedia.objects.all()
    )

    # Readable names in output
    movie_genre = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='name'
    )
    platform = serializers.SlugRelatedField(
        read_only=True, slug_field='platform'
    )
    movie_cast = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='castmedia__name'
    )
    movie_creator = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='creator_name'
    )
    movie_writer = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='writer_name'
    )

    # IDs for input only
    movie_genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Genre.objects.all(), 
        write_only=True, 
        source='movie_genre'
    )
    platform_id = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(), write_only=True, source='platform'
    )
    movie_cast_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Cast.objects.all(), write_only=True, source='movie_cast'
    )
    movie_creator_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Creator.objects.all(), write_only=True, source='movie_creator'
    )
    movie_writer_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Writer.objects.all(), write_only=True, source='movie_writer'
    )

    class Meta:
        model = Movie
        fields = [
            'id',
            'moviemedia',
            'title',
            'banners',
            'thumbnails',
            'trailers',
            'video',
            'related_pic',

            # ✅ Readable output
            'movie_genre',
            'platform',
            'movie_cast',
            'movie_creator',
            'movie_writer',

            # ✅ IDs only for input
            'movie_genre_ids',
            'platform_id',
            'movie_cast_ids',
            'movie_creator_ids',
            'movie_writer_ids',
            'movie_created',
            'movie_updated'
        ]



class MovieGeneralDetailSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset = Movie.objects.all(),
        source = 'movie',
        write_only=True 
    )

    class Meta: 
        model = MovieGeneralDetail
        fields = [
            'id',
            'movie',
            'movie_id',
            'active',
            'is_original',
            'duration',
            'avg_rating',
            'number_rating',
            'storyline'
        ]



class MovieCoreDetailSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True
    )

    language = serializers.SlugRelatedField(
        read_only=True,
        slug_field='language',
        many=True,
    )
    production_companies = serializers.SlugRelatedField(
        read_only=True,
        slug_field='production_company',
        many=True,
    )

    language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        many=True,
        write_only=True,
        source='language'
    )
    production_companies_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductionCompany.objects.all(),
        many=True,
        write_only=True,
        source='production_companies'
    )

    class Meta:
        model = MovieCoreDetail
        fields = [
            'id',
            'movie',
            'movie_id',
            'release_date',
            'country_of_origin',
            'also_known_as',
            'filming_location',

            # writable 
            'language_id',
            'production_companies_id',

            # readable : not shown while posting
            'language',
            'production_companies'
        ]




class MovieBoxOfficeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset = Movie.objects.all(),
        source = 'movie',
        write_only = True
    )

    class Meta: 
        model = MovieBoxOffice
        fields = [
            'id',
            'movie',
            'movie_id',
            'budget',
            'gross_country',
            'opening_weekend',
            'gross_worldwide'
        ]


class MovieTechSpecsSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset = Movie.objects.all(),
        source = 'movie',
        write_only=True
    )

    class Meta :
        model = MovieTechSpecs
        fields = [
            'id',
            'movie',
            'movie_id',
            'runtime',
            'color',
            'sound_mix'
        ]
    



class MovieRatingReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset = Movie.objects.all(),
        source = 'movie',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_movie_review = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_movie_review',
        write_only=True
    )

    class Meta:
        model = MovieRatingReview
        fields = [
            'id',
            'movie',
            'movie_id',

            #  readable
            'user_movie_review',

            #  writable
            'user_id',

            'rating',
            'review',
            'active',
            'created',
            'updated'
        ]



class MovieVotesSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset = Movie.objects.all(),
        source = 'movie',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_vote = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_vote',
        write_only=True
    )

    class Meta: 
        model = MovieVotes
        fields = [
            'id',
            'movie',
            'movie_id',

            # Readable 
            'user_vote',

            # Writable 
            'user_id',
            'vote_type',
            'voted_at'
        ]




class UserMovieWatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset = Movie.objects.all(),
        source = 'movie',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_watchlist = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_watchlist',
        write_only=True
    )

    class Meta: 
        model = UserMovieWatchlist
        fields = [
            'id',
            'movie',
            'movie_id',
            # readable
            'user_watchlist',

            # writable
            'user_id',

            'added_at',
            'removed_at'
        ]


class UserMovieViewedSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset = Movie.objects.all(),
        source = 'movie',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_viewed = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_viewed',
        write_only=True
    )

    class Meta: 
        model = UserMovieViewed
        fields = [
            'id',
            'movie',
            'movie_id',
            # writable 
            'user_id',

            # readable 
            'user_viewed',
            'viewed_at',
            'removed_at'
        ]



class MovieWatchHistorySerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = MovieWatchHistory
        fields = [
            'id',
            'movie',
            'movie_id',
            'user',
            'user_id',
            'watched_at',
            'duration_watched',
            'is_completed'
        ]
        