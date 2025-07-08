# serializers.py
from rest_framework import serializers
from app1_media_manger.models import MediaFile, EpisodeMedia
from app10_episode.models import ( 
    Episode, EpisodeGeneralDetail, EpisodeWatchlist,
    EpisodeViewed, EpisodeVotes, EpisodeRatingReview,
    EpisodeWatchHistory
)

from django.contrib.auth import get_user_model
User = get_user_model()
 
 


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MediaFile
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']
        ref_name = "app10-mediafilemanager"


class EpisodeSerializer(serializers.ModelSerializer):
    episode_number = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source='episodemedia.title', read_only=True)
    tvshow = serializers.CharField(source='episodemedia.tvshow.name', read_only=True)
    season = serializers.IntegerField(source='episodemedia.season.season_number', read_only=True)

    thumbnails = MediaFileSerializer(many=True, read_only=True)
    videos = MediaFileSerializer(many=True, read_only=True)

    # Write input: just one field
    episodemedia_slug = serializers.SlugRelatedField(
        queryset=EpisodeMedia.objects.all(),
        slug_field='episode_slug',
        write_only=True
    )

    class Meta: 
        model = Episode
        fields = [
            # For Output
            'id',
            'title',
            'episode_number',
            'tvshow',
            'season',
            'thumbnails',
            'videos',
            'episode_created',
            'episode_updated',

            # For Input
            'episodemedia_slug'
        ]

    def create(self, validated_data):
        episode_media = validated_data.pop('episodemedia_slug')

        # Prevent duplicate Episode creation
        if hasattr(episode_media, 'app10_episode'):
            raise serializers.ValidationError("An Episode object already exists for this EpisodeMedia.")

        episode = Episode.objects.create(episodemedia=episode_media)
        return episode



class EpisodeGeneralDetailSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer(read_only=True)
    episode_id = serializers.PrimaryKeyRelatedField(
        queryset = Episode.objects.all(),
        source='episode',
        write_only=True
    )

    class Meta: 
        model = EpisodeGeneralDetail
        fields = [
            'id',
            'episode',
            'episode_id',
            'active',
            'is_original',
            'avg_rating',
            'number_rating',
            'storyline'
        ]



class UserEpisodeWatchlistSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer(read_only=True)
    episode_id = serializers.PrimaryKeyRelatedField(
        queryset = Episode.objects.all(),
        source = 'episode',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_watchlist = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'user_watchlist',
        write_only=True
    )

    class Meta: 
        model = EpisodeWatchlist
        fields = [
            'id',
            'episode',
            'episode_id',
            #readable 
            'user_watchlist',

            #writable
            'user_id',

            'added_at',
            'removed_at'
        ]



class UserEpisodeViewedSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer(read_only=True)
    episode_id = serializers.PrimaryKeyRelatedField(
        queryset = Episode.objects.all(),
        source = 'episode',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_viewed = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'user_viewed',
        write_only=True
    )

    class Meta: 
        model = EpisodeViewed
        fields = [
            'id',
            'episode',
            'episode_id',
            #readable 
            'user_viewed',

            #writable
            'user_id',

            'viewed_at',
            'removed_at'
        ]



class EpisodeVotesSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer(read_only=True)
    episode_id = serializers.PrimaryKeyRelatedField(
        queryset = Episode.objects.all(),
        source = 'episode',
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
        model = EpisodeVotes
        fields = [
            'id',
            'episode',
            'episode_id',

            # Readable 
            'user_vote',

            # Writable 
            'user_id',
            'vote_type',
            'voted_at'
        ]


class EpisodeRatingReviewSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer(read_only=True)
    episode_id = serializers.PrimaryKeyRelatedField(
        queryset = Episode.objects.all(),
        source = 'episode',
        write_only=True
    )

    # Readable output (optional: use StringRelatedField or nested serializer)
    user_episode_review = serializers.StringRelatedField(read_only=True)

    # Input field for user
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_episode_review',
        write_only=True
    )

    class Meta:
        model = EpisodeRatingReview
        fields = [
            'id',
            'episode',
            'episode_id',

            #  readable
            'user_episode_review',

            #  writable
            'user_id',

            'rating',
            'review',
            'active',
            'created',
            'updated'
        ]


class EpisodeWatchHistorySerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer(read_only=True)
    episode_id = serializers.PrimaryKeyRelatedField(
        queryset=Episode.objects.all(),
        source='episode',
        write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = EpisodeWatchHistory
        fields = [
            'id',
            'episode',
            'episode_id',
            'user',
            'user_id',
            'watched_at',
            'duration_watched',
            'is_completed'
        ]
        

        