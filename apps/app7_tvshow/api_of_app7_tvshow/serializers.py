# serializers.py
from rest_framework import serializers 
from app1_media_manger.models import MediaFile, TVShowMedia
from app2_gener_platform.models import Genre, Platform
from app3_cast.models import Cast 
from app4_creator.models import Creator 
from app5_writer.models import Writer
from app8_lang_prod_company.models import Language, ProductionCompany

from app7_tvshow.models import ( 
    TvShow, TvShowGeneralDetail, TvShowCoreDetail, 
    TvShowTechSpecs, TvShowRatingReview, TvShowVotes, 
    UserTvShowWatchlist, UserTvShowViewed
)


from django.contrib.auth import get_user_model
User = get_user_model()

 

 

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MediaFile
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']
        ref_name = "app7-mediafilemanager"

'''
    Notes : 
        - castmedia__name means:
        - Go to the castmedia related model, and get its name field.
'''


class TvShowSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='tvshowmedia.name', read_only=True)
    banners = MediaFileSerializer(many=True, read_only=True)
    thumbnails = MediaFileSerializer(many=True, read_only=True)
    trailers = MediaFileSerializer(many=True, read_only=True)
    related_pic = MediaFileSerializer(many=True, read_only=True)
 

    tvshowmedia = serializers.SlugRelatedField(
        slug_field='tvshow_slug',
        queryset = TVShowMedia.objects.all()
    )

    # Readable names in output 
    tvshow_genre = serializers.SlugRelatedField(
        read_only=True, slug_field='name', many=True
    )

    platform = serializers.SlugRelatedField(
        read_only=True, slug_field='platform'
    )

    tvshow_cast = serializers.SlugRelatedField(
            many=True, 
            read_only=True,    
            slug_field='castmedia__name'  
    )

    tvshow_creator = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='creator_name'
    )

    tvshow_writer = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='writer_name'
    )

    # IDs for input only 
    tvhsow_genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Genre.objects.all(),
        write_only=True, 
        source='tvshow_genre'
    )

    platform_id = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(),
        write_only=True, 
        source='platform'
    )

    tvshow_cast_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Cast.objects.all(),
        write_only=True,
        source='tvshow_cast'
    )

    tvshow_creator_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Creator.objects.all(),
        write_only=True, 
        source='tvshow_creator'
    )

    tvshow_writer_ids = serializers.PrimaryKeyRelatedField(
        many= True, 
        queryset = Writer.objects.all(),
        write_only = True, 
        source = 'tvshow_writer'
    )

    class Meta: 
        model = TvShow
        fields = [
            'id',
            'tvshowmedia',
            'title',
            'banners',
            'thumbnails',
            'trailers',
            'related_pic',

            # ✅ Readable output
            'tvshow_genre',
            'platform',
            'tvshow_cast',
            'tvshow_creator',
            'tvshow_writer',

            # ✅ IDs only for input
            'tvhsow_genre_ids',
            'platform_id',
            'tvshow_cast_ids',
            'tvshow_creator_ids',
            'tvshow_writer_ids'
        ]
    




class TvshowGeneralDetailSerializer(serializers.ModelSerializer):
    tvshow = TvShowSerializer(read_only=True)
    tvshow_id = serializers.PrimaryKeyRelatedField(
        queryset = TvShow.objects.all(),
        source = 'tvshow',
        write_only=True
    )

    class Meta: 
        model = TvShowGeneralDetail
        fields = [
            'id',
            'tvshow',
            'tvshow_id',
            'active',
            'is_original',
            'avg_rating',
            'number_rating',
            'storyline'
        ]




class TvShowCoreDetailSerializer(serializers.ModelSerializer):
    tvshow = TvShowSerializer(read_only = True)
    tvshow_id = serializers.PrimaryKeyRelatedField(
        queryset=TvShow.objects.all(),
        source = 'tvshow',
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
        model = TvShowCoreDetail
        fields = [
            'id',
            'tvshow',
            'tvshow_id',
            'release_date',
            'country_of_origin',
            'also_known_as',
            'filming_location',

            #writable
            'language_id',
            'production_companies_id',

            #readbale
            'language',
            'production_companies'
        ]




class TvShowTechSpecsSerializer(serializers.ModelSerializer):
    tvshow = TvShowSerializer(read_only=True)
    tvshow_id = serializers.PrimaryKeyRelatedField(
        queryset = TvShow.objects.all(),
        source = 'tvshow',
        write_only=True
    )

    class Meta :
        model = TvShowTechSpecs
        fields = [
            'id',
            'tvshow',
            'tvshow_id',
            'runtime',
            'color',
            'sound_mix'
        ]
    


class TvShowRatingReviewSerializer(serializers.ModelSerializer):
    tvshow = TvShowSerializer(read_only=True)
    tvshow_id = serializers.PrimaryKeyRelatedField(
        queryset = TvShow.objects.all(),
        source = 'tvshow',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_tvshow_review = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_tvshow_review',
        write_only=True
    )

    class Meta:
        model = TvShowRatingReview
        fields = [
            'id',
            'tvshow',
            'tvshow_id',

            #  readable
            'user_tvshow_review',

            #  writable
            'user_id',

            'rating',
            'review',
            'active',
            'created',
            'updated'
        ]



class TvShowVotesSerializer(serializers.ModelSerializer):
    tvshow = TvShowSerializer(read_only=True)
    tvshow_id = serializers.PrimaryKeyRelatedField(
        queryset = TvShow.objects.all(),
        source = 'tvshow',
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
        model = TvShowVotes
        fields = [
            'id',
            'tvshow',
            'tvshow_id',

            # Readable 
            'user_vote',

            # Writable 
            'user_id',
            'vote_type',
            'voted_at'
        ]



class UserTvShowWatchlistSerializer(serializers.ModelSerializer):
    tvshow = TvShowSerializer(read_only=True)
    tvshow_id = serializers.PrimaryKeyRelatedField(
        queryset = TvShow.objects.all(),
        source = 'tvshow',
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
        model = UserTvShowWatchlist
        fields = [
            'id',
            'tvshow',
            'tvshow_id',
            # readable
            'user_watchlist',

            # writable
            'user_id',

            'added_at',
            'removed_at'
        ]

 



class UserTvShowViewedSerializer(serializers.ModelSerializer):
    tvshow = TvShowSerializer(read_only=True)
    tvshow_id = serializers.PrimaryKeyRelatedField(
        queryset = TvShow.objects.all(),
        source = 'tvshow',
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
        model = UserTvShowViewed
        fields = [
            'id',
            'tvshow',
            'tvshow_id',

            # writable 
            'user_id',

            # readable 
            'user_viewed',
            'viewed_at',
            'removed_at'
        ]

