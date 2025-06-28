# views.py
from rest_framework import generics , status
from rest_framework.response import Response
from app10_episode.models import ( 
    Episode,  EpisodeGeneralDetail , EpisodeWatchlist,
    EpisodeViewed, EpisodeVotes, EpisodeRatingReview
)

from app10_episode.api_of_app10_episode.serializers import ( 
    EpisodeSerializer , EpisodeGeneralDetailSerializer, 
    UserEpisodeWatchlistSerializer, UserEpisodeViewedSerializer, 
    EpisodeVotesSerializer, EpisodeRatingReviewSerializer
)

# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : Episode APIs'], operation_id='list all episode available',
    operation_description='list all episode available',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App10 : Episode APIs'], operation_id='create an episode',
    operation_description='create an episode',
)) 
class Episode_LC_View(generics.ListCreateAPIView):
    queryset = Episode.objects.all().select_related('episodemedia').prefetch_related('episodemedia__media_files')
    serializer_class = EpisodeSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : Episode APIs'], operation_id='retrieve particular episode detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App10 : Episode APIs'], operation_id='update particular episode detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App10 : Episode APIs'], operation_id='patch particular episode detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App10 : Episode APIs'], operation_id='delete particular episode detail',
))
class Episode_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.all().select_related('episodemedia').prefetch_related('episodemedia__media_files')
    serializer_class = EpisodeSerializer 




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : Episode General Detail APIs'], operation_id='list all episode general detail',
    operation_description='list all episode general detail',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App10 : Episode General Detail APIs'], operation_id='create an episode general detail',
    operation_description='create an episode general detail',
)) 
class EpisodeGeneralDetail_LC_View(generics.ListCreateAPIView):
    queryset = EpisodeGeneralDetail.objects.all().select_related('episode')
    serializer_class = EpisodeGeneralDetailSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : Episode General Detail APIs'], operation_id='retrieve particular episode general detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App10 : Episode General Detail APIs'], operation_id='update particular episode general detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App10 : Episode General Detail APIs'], operation_id='patch particular episode general detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App10 : Episode General Detail APIs'], operation_id='delete particular episode general  detail',
))
class EpisodeGeneralDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = EpisodeGeneralDetail.objects.all().select_related('episode')
    serializer_class = EpisodeGeneralDetailSerializer

 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : Episode Watchlist APIs'], operation_id='list all episode watchlist',
    operation_description='list all episode watchlist',
))
class EpisodeUserWatchlist_LC_View(generics.ListAPIView):
    queryset = EpisodeWatchlist.objects.all().select_related('episode')
    serializer_class = UserEpisodeWatchlistSerializer



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App10 : Episode Watchlist APIs'], operation_id='create a user watchlist',
    operation_description='create a user watchlist',
)) 
class UserEpisodeWatchlistToggleView(generics.CreateAPIView):
    serializer_class = UserEpisodeWatchlistSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        episode = request.data.get('episode_id')

        # check for existing entry
        existing = EpisodeWatchlist.objects.filter(user_watchlist_id=user, episode_id=episode).first()

        if existing: 
            existing.delete()
            return Response({
                'detail': 'Removed from watchlist'
            }, status = status.HTTP_200_OK)
        else: 
            # Create new watchlist entry 
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )





@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : Users Episode Viewing History APIs'], operation_id='see what user viewed',
    operation_description='see what user viewed',
))
class EpisodeUserViewed_LC_View(generics.ListAPIView):
    queryset = EpisodeViewed.objects.all().select_related('episode')
    serializer_class = UserEpisodeViewedSerializer



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App10 : Users Episode Viewing History APIs'], operation_id='make an episode as viewed',
    operation_description='make an episode as viewed',
)) 
class UserEpisodeViewedToggleView(generics.CreateAPIView):
    serializer_class = UserEpisodeViewedSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        episode = request.data.get('episode_id')

        # check for existing entry
        existing = EpisodeViewed.objects.filter(user_viewed_id=user, episode_id=episode).first()

        if existing: 
            existing.delete()
            return Response({
                'detail': 'Removed from viewing history'
            }, status = status.HTTP_200_OK)
        else: 
            # Create new watchlist entry 
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : Episode User Votes APIs'], operation_id='list all episode votes',
    operation_description='list all episode votes', 
))
class EpisodeVotes_List_View(generics.ListAPIView):
    queryset = EpisodeVotes.objects.all().select_related('episode')
    serializer_class = EpisodeVotesSerializer




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App10 : Episode User Votes APIs'], operation_id='give vote on an episode',
    operation_description='give vote on an episode',
)) 
class EpisodeVotesToggleView(generics.CreateAPIView):
    serializer_class = EpisodeVotesSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        episode = request.data.get('episode_id')

        # Check for existing entry
        existing = EpisodeVotes.objects.filter(user_vote_id=user, episode_id=episode).first()

        if existing:
            existing.delete()
            return Response({'detail': 'user removed the vote.'}, status=status.HTTP_200_OK)
        else:
            # Create new watchlist entry
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : EpisodeRatingReview APIs'], operation_id='list episode rating and review',
    operation_description='list episode rating and review', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App10 : EpisodeRatingReview APIs'], operation_id='create an episode rating and review',
    operation_description='create an episode rating and review', 
))
class EpisodeRatingReview_LC_View(generics.ListCreateAPIView):
    queryset = EpisodeRatingReview.objects.all().select_related('episode')
    serializer_class = EpisodeRatingReviewSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App10 : EpisodeRatingReview APIs'], operation_id='retrieve particular episode rating and review',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App10 : EpisodeRatingReview APIs'], operation_id='update particular episode rating and review',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App10 : EpisodeRatingReview APIs'], operation_id='patch particular episode rating and review',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App10 : EpisodeRatingReview APIs'], operation_id='delete particular episode rating and review',
))
class EpisodeRatingReview_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = EpisodeRatingReview.objects.all().select_related('episode')
    serializer_class = EpisodeRatingReviewSerializer


