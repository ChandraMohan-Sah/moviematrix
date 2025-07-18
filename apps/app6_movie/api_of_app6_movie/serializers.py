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
 
from rest_framework.exceptions import ValidationError

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


class MediaFileMixin:
    def get_media(self, obj, media_type):
        media_list = list(obj.media_files.all()) # 'media_files' must be prefetched on the queryset to avoid extra DB queries
        
        filtered_media = []
        for m in media_list:
            if m.media_type == media_type:
                filtered_media.append(m)

        return MediaFileSerializer(filtered_media, many=True).data


''' ------------Find the reason why its not optimized---------------'''
# # --- WRITE SERIALIZER (for POST/PUT/PATCH) ---
# class MovieWriteSerializer(serializers.ModelSerializer):
#     moviemedia = serializers.SlugRelatedField(
#         slug_field='movie_slug',
#         queryset=MovieMedia.objects.only('id', 'movie_slug'),
#         write_only=True
#     )
#     movie_genre_ids = serializers.PrimaryKeyRelatedField(
#         many=True, 
#         queryset=Genre.objects.only('id'), 
#         write_only=True, 
#         source='movie_genre'
#     )
#     platform_id = serializers.PrimaryKeyRelatedField(
#         queryset=Platform.objects.only('id'), 
#         write_only=True, 
#         source='platform'
#     )
#     movie_cast_ids = serializers.PrimaryKeyRelatedField(
#         many=True, 
#         queryset=Cast.objects.only('id'), 
#         write_only=True, 
#         source='movie_cast'
#     )
#     movie_creator_ids = serializers.PrimaryKeyRelatedField(
#         many=True, 
#         queryset=Creator.objects.only('id'), 
#         write_only=True, 
#         source='movie_creator'
#     )
#     movie_writer_ids = serializers.PrimaryKeyRelatedField(
#         many=True, 
#         queryset=Writer.objects.only('id'), 
#         write_only=True, source='movie_writer'
#     )

#     class Meta:
#         model = Movie
#         fields = [
#             'moviemedia',
#             'movie_genre_ids',
#             'platform_id',
#             'movie_cast_ids',
#             'movie_creator_ids',
#             'movie_writer_ids',
#         ]
#         ref_name = 'app6-moviewriteserializer'



class MovieSerializer(serializers.ModelSerializer, MediaFileMixin):
    class Meta :
        model = Movie
        fields = [
            'id', 'title', 'moviemedia', 'movie_genre', 'platform',
            'movie_cast', 'movie_creator', 'movie_writer',
            'movie_created', 'movie_updated'
        ]
    pass



'''Notes :
    -------------------------------------------------------------------------------------------------------------------------------
    | Part                               | Meaning                                                                                |
    |------------------------------------|--------------------------------------------------------------------------------------- |
    | `ListField(...)`                   | The incoming value must be a **list**                                                  |
    | `child=serializers.IntegerField()` | Each item in the list must be an **integer**                                           |
    | `write_only=True`                  | Don't show this in output (e.g., GET responses), only accept in input (POST/PUT/PATCH) |
    -------------------------------------------------------------------------------------------------------------------------------
'''
class MovieWriteSerializer(serializers.ModelSerializer):
    moviemedia_slug = serializers.SlugField(write_only=True)
    movie_genre_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    platform_id = serializers.IntegerField(write_only=True)
    movie_cast_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    movie_creator_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    movie_writer_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Movie
        fields = [
            'moviemedia_slug',
            'movie_genre_ids',
            'platform_id',
            'movie_cast_ids',
            'movie_creator_ids',
            'movie_writer_ids',
        ]
        ref_name = 'app6-moviewriteserializer'

    def create(self, validated_data):
        # Pop relation fields
        moviemedia_slug = validated_data.pop('moviemedia_slug')
        movie_genre_ids = validated_data.pop('movie_genre_ids', [])
        platform_id = validated_data.pop('platform_id')
        movie_cast_ids = validated_data.pop('movie_cast_ids', [])
        movie_creator_ids = validated_data.pop('movie_creator_ids', [])
        movie_writer_ids = validated_data.pop('movie_writer_ids', [])

        # Fetch related objects with minimal queries
        moviemedia = MovieMedia.objects.only('id').get(movie_slug=moviemedia_slug)
        platform = Platform.objects.only('id').get(id=platform_id)

        # create an instance
        movie = Movie.objects.create(
            moviemedia=moviemedia,
            platform=platform,
            **validated_data
        )

        # In Many-to-many relationship : we don't need to set the m2m fields immediately.
        # .set :  replace all related genres with a new list in one call.
        ''' Notes: 
            - Normal Table :
                - one-to-one and foreign key  relationships 
                    : are shown by adding a separate column in main table
                    : so mandatory to include these fields during creation
                    

                - many-to many relationsips 
                    : are shown by creating a separate join table
                    : these join tables are created automatically by Django
                    : and are hidden from the user

                    Join Table Needs the primary keys of both tables: 
                    : e.g., for Movie and Genre, the join table would look like this:
                    ---------------------
                    movie_id	genre_id
                        1	        3
                        1	        5
                        2	        3
                    -----------------------

            - many-to-many relationships are stored in a separate join table
            - Django: creates the main object first (e.g., a Movie) — this gives it a primary key (ID).
            - Then allows you to add many-to-many relationships later, using .set(), .add(), etc.
            - That's why it's not required to include M2M fields during the initial .create() call.
        '''
        movie.movie_genre.set(Genre.objects.filter(id__in=movie_genre_ids).only('id'))
        movie.movie_cast.set(Cast.objects.filter(id__in=movie_cast_ids).only('id'))
        movie.movie_creator.set(Creator.objects.filter(id__in=movie_creator_ids).only('id'))
        movie.movie_writer.set(Writer.objects.filter(id__in=movie_writer_ids).only('id'))

        return movie


    def update(self, instance, validated_data):
        # Pop relation fields (custom input fields)
        moviemedia_slug = validated_data.pop('moviemedia_slug', None)
        movie_genre_ids = validated_data.pop('movie_genre_ids', [])
        platform_id = validated_data.pop('platform_id', None)
        movie_cast_ids = validated_data.pop('movie_cast_ids', [])
        movie_creator_ids = validated_data.pop('movie_creator_ids', [])
        movie_writer_ids = validated_data.pop('movie_writer_ids', [])

        # Update FK fields if provided
        if moviemedia_slug:
            moviemedia = MovieMedia.objects.only('id').get(movie_slug=moviemedia_slug)
            instance.moviemedia = moviemedia

        '''
            “Go to the Platform table, and get the row where the id is equal to platform_id,
            but only fetch the id column — don't load other fields like name, slug, etc.”
        '''
        if platform_id:
            platform = Platform.objects.only('id').get(id=platform_id)
            instance.platform = platform

        # Save updated FK fields + any remaining fields
        instance.save()

        # Handling other fields for updation
        # For M2M: Use .set() to replace old relations with new ones
        if movie_genre_ids:
            instance.movie_genre.set(Genre.objects.filter(id__in=movie_genre_ids).only('id'))
        if movie_cast_ids:
            instance.movie_cast.set(Cast.objects.filter(id__in=movie_cast_ids).only('id'))
        if movie_creator_ids:
            instance.movie_creator.set(Creator.objects.filter(id__in=movie_creator_ids).only('id'))
        if movie_writer_ids:
            instance.movie_writer.set(Writer.objects.filter(id__in=movie_writer_ids).only('id'))

        return instance




# --- READ SERIALIZER (for GET) ---
class MovieReadSerializer(serializers.ModelSerializer, MediaFileMixin):
    movie_name = serializers.CharField(source='moviemedia.name', read_only=True)
    trailer = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    banners = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    related_pic = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField(source='movie_general_detail.avg_rating', read_only=True)


    # # m2m fields but optimized to fetch its name and id only
    # movie_genre = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='name',
    #     many=True,
    # )

    # platform = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='platform'
    # )

    # movie_cast = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='cast_name',
    #     many=True,
    # )

    # movie_creator = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='creator_name',
    #     many=True,
    # )   

    # movie_writer = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='writer_name',
    #     many=True,
    # )

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_name',
            'trailer',
            'video',
            'banners',
            'thumbnails',
            'related_pic',
            # 'movie_genre',
            # 'platform',
            # 'movie_cast',
            # 'movie_creator',
            # 'movie_writer',
            'avg_rating',
            'movie_created',
            'movie_updated',
        ]
        ref_name = 'app6-moviereadserializer'

    def get_trailer(self, obj):
        return self.get_media(obj.moviemedia, 'trailer')

    def get_video(self, obj):
        return self.get_media(obj.moviemedia, 'video')

    def get_banners(self, obj):
        return self.get_media(obj.moviemedia, 'banner')

    def get_thumbnails(self, obj):
        return self.get_media(obj.moviemedia, 'thumbnail')

    def get_related_pic(self, obj):
        return self.get_media(obj.moviemedia, 'related_pic')



# --- Write SERIALIZER (for POST, PUT, PATCH) ---
class MovieGeneralDetail_WriteSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MovieGeneralDetail
        fields = [
            'id', 'movie_id', 'active', 'is_original',
            'duration', 'avg_rating', 'number_rating', 'storyline'
        ]

    def create(self, validated_data):
        # Pop relation fields (foreign keys or m2m IDs) from validated_data
        movie_id = validated_data.pop('movie_id')

        # Check for existing MovieGeneralDetail for this movie
        if MovieGeneralDetail.objects.filter(movie_id=movie_id).exists():
            raise ValidationError(f"MovieGeneralDetail for movie_id {movie_id} already exists.")
        
        # Fetch related objects with minimal fields using .only('id')
        movie = Movie.objects.only('id').get(id=movie_id)

        # Create the instance with both direct and related data
        movie_general_detail = MovieGeneralDetail.objects.create(
            movie=movie,
            **validated_data
        )
        return movie_general_detail
    

    def update(self, instance, validated_data):
        # pop relation fields (custom input fields)
        movie_id = validated_data.pop('movie_id', None)

        # Update FK fields if provided
        if movie_id:
            movie = Movie.objects.only('id').get(id=movie_id)
            instance.movie = movie


        # Update all other fields dynamically
        for attr, value in validated_data.items():
            # setattr will update each field on the instance
            setattr(instance, attr, value)

        # Save updated FK fields + any remaining fields
        instance.save()
        return instance 
    

    
# --- READ SERIALIZER (for GET) ---
class MovieGenralDetail_ReadSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='movie.title', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    
    class Meta:
        model = MovieGeneralDetail 
        fields = [
            'id', 'movie_name', 'movie_id','active', 'is_original',
            'duration', 'avg_rating', 'number_rating', 'storyline'
        ]





# --- Write SERIALIZER (for POST, PUT, PATCH) ---
class MovieCoreDetail_WriteSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)
    language = serializers.ListField(
        child = serializers.IntegerField(),
        write_only=True
    )
    production_companies = serializers.ListField(
        child = serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = MovieCoreDetail
        fields =[
            'id', 'movie_id', 'release_date', 'country_of_origin',
            'also_known_as', 'filming_location', 'language', 'production_companies'
        ]

    def create(self, validated_data):
        # Pop relation fields (foreign keys or m2m IDs) from validated_data
        movie_id = validated_data.pop('movie_id')
        language_ids = validated_data.pop('language',[])
        production_company_ids = validated_data.pop('production_companies', [])

        # Check for existing MovieCoreDetail for this movie
        if MovieCoreDetail.objects.filter(movie_id=movie_id).exists():
            raise ValidationError(f"MovieCoreDetail for movie_id {movie_id} already exists.")
        
        # Fetch related objects with minimal fields using .only('id')
        movie = Movie.objects.only('id').get(id=movie_id)

        # Create the instance with both direct and related data
        movie_core_detail = MovieCoreDetail.objects.create(
            movie=movie,
            **validated_data
        )

        # Set Many-to-Many relationships
        movie_core_detail.language.set(Language.objects.filter(id__in=language_ids).only('id'))
        movie_core_detail.production_companies.set(ProductionCompany.objects.filter(id__in=production_company_ids).only('id'))
        return movie_core_detail
    
    def update(self, instance, validated_data):
        # pop relation fields (custom input fields)
        movie_id = validated_data.pop('movie_id', None)
        language_ids = validated_data.pop('language', [])
        production_company_ids = validated_data.pop('production_companies', [])

        # Update FK fields if provided
        if movie_id:
            movie = Movie.objects.only('id').get(id=movie_id)
            instance.movie = movie

        # Update all other fields dynamically
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save updated FK fields + any remaining fields
        instance.save()

        # Set Many-to-Many relationships
        if language_ids:
            instance.language.set(Language.objects.filter(id__in=language_ids).only('id'))
        if production_company_ids:
            instance.production_companies.set(ProductionCompany.objects.filter(id__in=production_company_ids).only('id'))

        return instance

 

class MovieCoreDetail_ReadSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='movie.title', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)

    # m2m fields but optimized to fetcch its name and id only
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

    class Meta: 
        model = MovieCoreDetail
        fields = [
            'id', 'movie_name','movie_id', 'release_date', 'country_of_origin',
            'also_known_as', 'filming_location', 
            'language', 'production_companies',
        ]



class MovieBoxOffice_WriteSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)

    class Meta: 
        model = MovieBoxOffice
        fields = [
            'id',
            'movie_id',
            'budget',
            'gross_country',
            'opening_weekend',
            'gross_worldwide'
        ]

    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')

        if MovieBoxOffice.objects.filter(movie_id=movie_id).exists():
            raise ValidationError(f"MovieBoxOffice for movie_id {movie_id} already exists.")
        
        movie = Movie.objects.only('id').get(id=movie_id)

        movie_box_office = MovieBoxOffice.objects.create(
            movie=movie,
            **validated_data
        )
        return movie_box_office
    
    
    def update(self, instance, validated_data):
        movie_id = validated_data.pop('movie_id', None)

        if movie_id:
            movie = Movie.objects.only('id').get(id=movie_id)
            instance.movie = movie

        # Update all other fields dynamically
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save updated FK fields + any remaining fields
        instance.save()
        return instance




class MovieBoxOffice_ReadSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='movie.title', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)

    class Meta: 
        model = MovieBoxOffice
        fields = [
            'id',
            'movie_name',
            'movie_id',
            'budget',
            'gross_country',
            'opening_weekend',
            'gross_worldwide'
        ]


class MovieTechSpecs_ReadSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source="movie.title", read_only=True)
    movie_id = serializers.IntegerField(source="movie.id", read_only=True)

    class Meta:
        model = MovieTechSpecs
        fields = [
            'id',
            'movie_name',
            'movie_id',
            'runtime',
            'color',
            'sound_mix'
        ]



class MovieTechSpecs_WriteSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MovieTechSpecs
        fields = [
            'id',
            'movie_id',
            'runtime',
            'color',
            'sound_mix'
        ]
    
    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')

        if MovieTechSpecs.objects.filter(movie_id=movie_id).exists():
            raise ValidationError(f"MovieTechSpecs for movie_id {movie_id} already exists.")
        
        movie = Movie.objects.only('id').get(id=movie_id)

        movie_tech_specs = MovieTechSpecs.objects.create(
            movie=movie,         # assign the foreign key object
            **validated_data     # remaining fields are assigned directly
        )
        return movie_tech_specs


    def update(self, instance, validated_data):
        movie_id = validated_data.pop('movie_id', None)

        if movie_id:
            movie = Movie.objects.only('id').get(id=movie_id)
            instance.movie = movie

        # Update all other fields dynamically
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save updated FK fields + any remaining fields
        instance.save()
        return instance
    
  
class MovieRatingReview_ReadSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='movie.title', read_only=True) 
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    user_movie_review = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user_movie_review.id', read_only=True)

    class Meta:
        model = MovieRatingReview
        fields = [
            'id',
            'movie_name',
            'movie_id',
            'user_movie_review',
            'user_id',
            'rating',
            'review',
            'active',
            'created',
            'updated'
        ]


class MovieRatingReview_WriteSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MovieRatingReview
        fields = [
            'id',
            'movie_id',
            'rating',
            'review',
            'active'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        
        movie_id = validated_data.pop('movie_id')

        # if MovieRatingReview.objects.filter(movie_id=movie_id, user_movie_review=user).exists():
        #     raise ValidationError(f"User {user.id} has already reviewed movie {movie_id}.")

        movie = Movie.objects.only('id').get(id=movie_id)

        return MovieRatingReview.objects.create(
            movie=movie,
            user_vote=user,
            **validated_data
        )


    def update(self, instance, validated_data):
        movie_id = validated_data.pop('movie_id', None)
        if movie_id:
            movie = Movie.objects.only('id').get(id=movie_id)
            instance.movie = movie

        # Use request user as the reviewer (if needed)
        user = self.context.get('request').user
        instance.user_movie_review = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class MovieVotes_ReadSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='movie.title', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    user_vote = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user_vote.id', read_only=True)

    class Meta:
        model = MovieVotes
        fields = [
            'id',
            'movie_name',
            'movie_id',
            'user_vote',
            'user_id',
            'vote_type',
            'voted_at'
        ]


class MovieVotes_WriteSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MovieVotes
        fields = [
            'id',
            'movie_id',
            'vote_type'
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        
        movie_id = validated_data.pop('movie_id')

        # Check if the user has already voted for this movie
        if MovieVotes.objects.filter(movie_id=movie_id, user_vote=user).exists():
            raise ValidationError(f"{user} has already voted for movie {movie_id}.")

        movie = Movie.objects.only('id').get(id=movie_id)

        return MovieVotes.objects.create(
            movie=movie,
            user_vote = user,
            **validated_data
        )



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


class MovieWatchHistory_ReadSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='movie.title', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)

    class Meta:
        model = MovieWatchHistory
        fields = [
            'id',
            'movie_name',
            'movie_id',
            'user',
            'user_id',
            'watched_at',
            'duration_watched',
            'is_completed'
        ]



class MovieWatchHistory_WriteSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MovieWatchHistory
        fields = [
            'id',
            'movie_id',
            'watched_at',
            'duration_watched',
            'is_completed'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        movie_id = validated_data.pop('movie_id')

        # 🔍 Check for existing watch history
        if MovieWatchHistory.objects.filter(movie_id=movie_id, user=user).exists():
            raise ValidationError(f"{user} has already watched movie {movie_id}.")

        movie = Movie.objects.only('id').get(id=movie_id)

        return MovieWatchHistory.objects.create(
            movie=movie,
            user=user,
            **validated_data
        )

    def update(self, instance, validated_data):
        movie_id = validated_data.pop('movie_id', None)
        if movie_id:
            instance.movie = Movie.objects.only('id').get(id=movie_id)

        # No need to update user — it's tied to login
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class LightMovieSerializer(serializers.ModelSerializer, MediaFileMixin):
    movie_name = serializers.CharField(source='moviemedia.name', read_only=True)
    thumbnails = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField(source='movie_general_detail.avg_rating', read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_name',
            'thumbnails',
            'avg_rating',
        ]
    
    def get_thumbnails(self, obj):
        return self.get_media(obj.moviemedia, 'thumbnail')


class MovieDetailSerializer(serializers.ModelSerializer, MediaFileMixin):
    title = serializers.CharField(source='moviemedia.name', read_only=True)
    year = serializers.CharField(source='movie_core_detail.release_year', read_only=True)
    rating = serializers.CharField(source='movie_general_detail.content_rating', default="Not Rated", read_only=True)
    duration = serializers.FloatField(source='movie_general_detail.duration', read_only=True)
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source='movie_genre')
    imdbRating = serializers.FloatField(source='movie_general_detail.avg_rating', read_only=True)
    ratingCount = serializers.CharField(source='movie_general_detail.number_rating', default="0", read_only=True)

    # Thumbnails and Backdrop
    poster = serializers.SerializerMethodField()
    backdrop = serializers.SerializerMethodField()


    plot = serializers.CharField(source='movie_general_detail.storyline', default="", read_only=True)
    director = serializers.SerializerMethodField()
    writers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='writer_name', source='movie_writer')
    stars = serializers.SerializerMethodField()

    cast = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    technicalSpecs = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'year', 'rating', 'duration',  'genres', 'imdbRating', 'ratingCount',
            'poster', 'backdrop', 'plot', 'director', 'writers',
            'stars', 'cast', 'photos', 'videos', 'reviews', 'technicalSpecs'
        ]


    def get_poster(self, obj):
        thumbnails = self.get_media(obj.moviemedia, 'thumbnail')
        return thumbnails[0]['cdn_url'] if thumbnails else "/placeholder.svg"

    def get_backdrop(self, obj):
        thumbnails = self.get_media(obj.moviemedia, 'thumbnail')
        if len(thumbnails) > 1:
            return thumbnails[1]['cdn_url']
        elif thumbnails:
            return thumbnails[0]['cdn_url']
        return "/placeholder.svg"


    def get_director(self, obj):
        director = obj.movie_creator.first()
        return director.creator_name if director else "Unknown"

    def get_stars(self, obj):
        return [cast.cast_name for cast in obj.movie_cast.all()[:3]]


    def get_cast(self, obj):
        return [
            {
                'id': cast.id,
                'name': cast.cast_name,
                'image': cast.profile_pic.first().cdn_url if cast.profile_pic.exists() else "/placeholder.svg"
            }
            for cast in obj.movie_cast.all()
        ]

    def get_photos(self, obj):
        return [thumb['cdn_url'] for thumb in self.get_media(obj.moviemedia, 'thumbnail')]

    def get_videos(self, obj):
        return self.get_media(obj.moviemedia, 'video')

    def get_reviews(self, obj):
        return MovieRatingReview_ReadSerializer(obj.movie_reviews.all(), many=True).data

    def get_technicalSpecs(self, obj):
        tech = getattr(obj, 'movie_tech_specs', None)
        return {
            "runtime": tech.runtime if tech else "",
            "soundMix": tech.sound_mix if tech else "Dolby Digital",
            "color": tech.color if tech else "Color",
        }




# class MovieWatchHistorySerializer(serializers.ModelSerializer):
#     movie = MovieSerializer(read_only=True)
#     movie_id = serializers.PrimaryKeyRelatedField(
#         queryset=Movie.objects.all(),
#         source='movie',
#         write_only=True
#     )
#     user = serializers.StringRelatedField(read_only=True)
#     user_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         source='user',
#         write_only=True
#     )

#     class Meta:
#         model = MovieWatchHistory
#         fields = [
#             'id',
#             'movie',
#             'movie_id',
#             'user',
#             'user_id',
#             'watched_at',
#             'duration_watched',
#             'is_completed'
#         ]
        