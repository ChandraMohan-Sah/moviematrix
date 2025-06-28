# views.py
from app7_tvshow.models import (
    TvShow , TvShowGeneralDetail, TvShowCoreDetail, 
    TvShowTechSpecs, TvShowRatingReview, TvShowVotes,
    UserTvShowWatchlist, UserTvShowViewed
)
from .serializers import (
    TvShowSerializer, TvshowGeneralDetailSerializer, TvShowCoreDetailSerializer,
    TvShowTechSpecsSerializer, TvShowRatingReviewSerializer, TvShowVotesSerializer,
    UserTvShowWatchlistSerializer, UserTvShowViewedSerializer
)

from rest_framework import generics, status 
from rest_framework.response import Response 
 
 
# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='list all tvshow',
    operation_description='list all tvshow', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='create a tvshow',
    operation_description='create a tvshow', 
))
class TvShow_LC_View(generics.ListCreateAPIView):
    queryset = TvShow.objects.all().select_related('tvshowmedia').prefetch_related('tvshowmedia__media_files')
    serializer_class = TvShowSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='retrieve particular tvshow detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='update particular tvshow detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='patch particular tvshow detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='delete particular tvshow detail',
))
class TvShow_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShow.objects.all().select_related('tvshowmedia').prefetch_related('tvshowmedia__media_files')
    serializer_class = TvShowSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='list tvshow general detail',
    operation_description='list all tvshow general detail', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='create a tvshow general detail',
    operation_description='create a tvshow general detail ', 
))
class TvShowGeneralDetail_LC_View(generics.ListCreateAPIView):
    queryset = TvShowGeneralDetail.objects.all().select_related('tvshow')
    serializer_class = TvshowGeneralDetailSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='retrieve particular tvshow general detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='update particular tvshow general detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='patch particular tvshow general detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='delete particular tvshow general  detail',
))
class TvShowGeneralDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowGeneralDetail.objects.all().select_related('tvshow')
    serializer_class = TvshowGeneralDetailSerializer






@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='list tvshow core detail',
    operation_description='list all tvshow core detail', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='create a tvshow core detail',
    operation_description='create a tvshow core detail ', 
))
class TvShowCoreDetail_LC_View(generics.ListCreateAPIView):
    queryset = TvShowCoreDetail.objects.all().select_related('tvshow')
    serializer_class = TvShowCoreDetailSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='retrieve particular tvshow core detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='update particular tvshow core detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='patch particular tvshow core detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='delete particular tvshow core  detail',
))
class TvShowCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowCoreDetail.objects.all().select_related('tvshow')
    serializer_class = TvShowCoreDetailSerializer


 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='list tvshow tech specs',
    operation_description='list all tvshow tech specs', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='create a tvshow tech specs',
    operation_description='create a tvshow tech specs ', 
))
class TvShowTechSpecsDetail_LC_View(generics.ListCreateAPIView):
    queryset = TvShowTechSpecs.objects.all().select_related('tvshow')
    serializer_class = TvShowTechSpecsSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='retrieve particular tvshow tech specs',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='update particular tvshow tech specs',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='patch particular tvshow tech specs',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='delete particular tvshow tech specs',
))
class TvShowTechSpecsDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowTechSpecs.objects.all().select_related('tvshow')
    serializer_class = TvShowTechSpecsSerializer




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='list tvshow rating and review',
    operation_description='list tvshow rating and review', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='create a tvshow rating and review',
    operation_description='create a tvshow rating and review', 
))
class TvShowRatingReview_LC_View(generics.ListCreateAPIView):
    queryset = TvShowRatingReview.objects.all().select_related('tvshow')
    serializer_class = TvShowRatingReviewSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='retrieve particular tvshow rating and review',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='update particular tvshow rating and review',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='patch particular tvshow rating and review',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='delete particular tvshow rating and review',
))
class TvShowRatingReview_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowRatingReview.objects.all().select_related('tvshow')
    serializer_class = TvShowRatingReviewSerializer




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserVotes APIs'], operation_id='list all tvshow votes',
    operation_description='list all tvshow votes', 
))
class TvShowVotes_List_View(generics.ListAPIView):
    queryset = TvShowVotes.objects.all().select_related('tvshow')
    serializer_class = TvShowVotesSerializer




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserVotes APIs'], operation_id='give vote on tvshow',
    operation_description='give vote on tvshow',
)) 
class UserTvShowVotesToggleView(generics.CreateAPIView):
    serializer_class = TvShowVotesSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        tvshow = request.data.get('tvshow_id')

        # Check for existing entry
        existing = TvShowVotes.objects.filter(user_vote_id=user, tvshow_id=tvshow).first()

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
    tags=['App7 : TvShowUserWatchlist APIs'], operation_id='list all user tvshow  watchlist',
    operation_description='list all user tvshow watchlist',
))
class UserTvShowWatchlist_List_View(generics.ListAPIView):
    queryset = UserTvShowWatchlist.objects.all().select_related('tvshow')
    serializer_class = UserTvShowWatchlistSerializer




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserWatchlist APIs'], operation_id='create a user watchlist',
    operation_description='create a user watchlist',
)) 
class UserTvShowWatchlistToggleView(generics.CreateAPIView):
    serializer_class = UserTvShowWatchlistSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        tvshow = request.data.get('tvshow_id')

        # Check for existing entry
        existing = UserTvShowWatchlist.objects.filter(user_watchlist_id=user, tvshow_id=tvshow).first()

        if existing:
            existing.delete()
            return Response({'detail': 'Removed from watchlist'}, status=status.HTTP_200_OK)
        else:
            # Create new watchlist entry
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)





@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserViewed APIs'], operation_id='list all user viewing list',
    operation_description='list all user viewing list',
))
class UserTvShowViewed_List_View(generics.ListAPIView):
    queryset = UserTvShowViewed.objects.all().select_related('tvshow')
    serializer_class = UserTvShowViewedSerializer



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserViewed APIs'], operation_id='create a user viewing history',
    operation_description='create a user viewing history',
)) 
class UserTvShowViewedToggleView(generics.CreateAPIView):
    serializer_class = UserTvShowViewedSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        tvshow = request.data.get('tvshow_id')

        # Check for existing entry
        existing = UserTvShowViewed.objects.filter(user_viewed_id=user, tvshow_id=tvshow).first()

        if existing:
            existing.delete()
            return Response({'detail': 'Removed from viewing history'}, status=status.HTTP_200_OK)
        else:
            # Create new watchlist entry
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


