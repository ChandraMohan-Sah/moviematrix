# serializers.py
from rest_framework import serializers
from app6_movie.models import Movie, UserMovieWatchlist
from app3_cast.models import Cast
from app4_creator.models import Creator
from app5_writer.models import Writer


'''
- Notes: how getattr() wroks
-------------------------------------------------------------------
    syntax:
        getattr(object, 'attribute_name', default_value)
-------------------------------------------------------------------
    class Book:
        title = "Django for Beginners"
        
    book = Book()

    # Access existing attribute
    print(getattr(book, 'title'))  # ➜ "Django for Beginners"

    # Access non-existing attribute with default fallback
    print(getattr(book, 'author', 'Unknown'))  # ➜ "Unknown"
-------------------------------------------------------------------

'''

class MovieTitleSerializer(serializers.ModelSerializer):
    """Serializer for Movie titles."""
    movie_rating = serializers.SerializerMethodField()
    is_watchlisted = serializers.SerializerMethodField()
    movie_storyline = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    release_date = serializers.DateField(source='movie_core_detail.release_date', read_only=True)
    duration = serializers.IntegerField(source='movie_general_detail.duration', read_only=True)
    also_known_as = serializers.CharField(source='movie_core_detail.also_known_as', read_only=True)


    class Meta:
        model = Movie
        fields = ['id', 'title', 'movie_rating', 'is_watchlisted', 'movie_storyline', 'release_date', 'duration', 'also_known_as', 'thumbnail',
                  ]

    def get_movie_rating(self, obj):
        """Get the average rating of the movie."""
        return obj.movie_general_detail.avg_rating if hasattr(obj, 'movie_general_detail') else None
    
    def get_is_watchlisted(self, obj):
        return obj.id in self.context.get('watchlisted_ids', set())
    
    def get_movie_storyline(self, obj):
        return obj.movie_general_detail.storyline if hasattr(obj, 'movie_general_detail') else None
  
    def get_thumbnail(self, obj):
        files = getattr(obj.moviemedia, 'media_files', None)
        if files:
            thumb = next((f for f in files.all() if f.media_type == 'thumbnail'), None)
            return thumb.cdn_url or thumb.file.url if thumb else None
        return None


    

class LightCastSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    other_work = serializers.SerializerMethodField()

    """Lightweight serializer for Cast."""
    class Meta:
        model = Cast
        fields = ['id', 'cast_name', 'profile_pic', 'dob', 'other_work']


    def get_profile_pic(self, obj):
        """Get the profile picture URL of the cast member."""
        files = getattr(obj.castmedia, 'media_files', None)
        if files:
            profile_pic = next((f for f in files.all() if f.media_type == 'profile_pic'), None)
            return profile_pic.cdn_url or profile_pic.file.url if profile_pic else None
        return None

    def get_dob(self, obj):
        return obj.core_detail.born_date if hasattr(obj, 'core_detail') else None

    def get_other_work(self, obj):
        return obj.core_detail.otherwork if hasattr(obj, 'core_detail') else None

    def get_other_work(self, obj):
        if hasattr(obj, 'cast_core_detail') and obj.cast_core_detail:
            return obj.cast_core_detail.otherwork
        return []



class LightCreatorSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    other_work = serializers.SerializerMethodField()

    class Meta:
        model = Creator
        fields = ['id', 'creator_name', 'profile_pic', 'dob', 'other_work']

    def get_profile_pic(self, obj):
        files = getattr(obj.creatormedia, 'media_files', None)
        if files:
            media_list = list(files) if hasattr(files, '__iter__') else files.all()
            profile_pic = next((f for f in media_list if f.media_type == 'profile_pic'), None)
            return profile_pic.cdn_url or profile_pic.file.url if profile_pic else None
        return None

    def get_dob(self, obj):
        if hasattr(obj, 'creator_core_detail') and obj.creator_core_detail:
            return obj.creator_core_detail.born_date
        return None

    def get_other_work(self, obj):
        if hasattr(obj, 'creator_core_detail') and obj.creator_core_detail:
            return obj.creator_core_detail.otherwork
        return []


class LightWriterSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    other_work = serializers.SerializerMethodField()

    class Meta:
        model = Writer
        fields = ['id', 'writer_name', 'profile_pic', 'dob', 'other_work']

    def get_profile_pic(self, obj):
        files = getattr(obj.writermedia, 'media_files', None)
        if files:
            media_list = list(files) if hasattr(files, '__iter__') else files.all()
            profile_pic = next((f for f in media_list if f.media_type == 'profile_pic'), None)
            return profile_pic.cdn_url or profile_pic.file.url if profile_pic else None
        return None

    def get_dob(self, obj):
        if hasattr(obj, 'writer_core_detail') and obj.writer_core_detail:
            return obj.writer_core_detail.born_date
        return None

    def get_other_work(self, obj):
        if hasattr(obj, 'writer_core_detail') and obj.writer_core_detail:
            return obj.writer_core_detail.otherwork
        return []
    