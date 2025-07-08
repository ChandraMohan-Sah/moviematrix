# views.py
from app7_tvshow.models import (
    TvShow , TvShowGeneralDetail, TvShowCoreDetail, 
    TvShowTechSpecs, TvShowRatingReview, TvShowVotes,
    UserTvShowWatchlist, UserTvShowViewed, TvShowWatchHistory
)
from .serializers import (
    TvShowSerializer, TvshowGeneralDetailSerializer, TvShowCoreDetailSerializer,
    TvShowTechSpecsSerializer, TvShowRatingReviewSerializer, TvShowVotesSerializer,
    UserTvShowWatchlistSerializer, UserTvShowViewedSerializer, TvShowWatchHistorySerializer
)

from rest_framework import generics, status 
from rest_framework.response import Response 
 
#pagination 
from rest_framework import pagination
from shared.pagination import GlobalPagination

#permissions
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from shared.permissions import IsAdminOrReadOnly
from .custom_permission import (
    IsTVShowReviewer_OrReadOnly, IsTvShowVoter_OrReadOnly,
    IsUserTvShowWatchlist_OrReadOnly, IsAdminOrUserWatchlistedTvShow, 
    IsUserViewedTvshow_OrReadOnly, IsAdminOrUserViewedTvShow
)


# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='list all tvshow [IsAdminOrReadOnly]',
    operation_description='list all tvshow', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='create a tvshow [IsAdminOrReadOnly]',
    operation_description='create a tvshow', 
))
class TvShow_LC_View(generics.ListCreateAPIView):
    queryset = TvShow.objects.all().select_related('tvshowmedia').prefetch_related('tvshowmedia__media_files')
    serializer_class = TvShowSerializer
    permission_classes = [IsAdminOrReadOnly]


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='retrieve particular tvshow detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='update particular tvshow detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='patch particular tvshow detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShow APIs'], operation_id='delete particular tvshow detail [IsAdminOrReadOnly]',
))
class TvShow_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShow.objects.all().select_related('tvshowmedia').prefetch_related('tvshowmedia__media_files')
    serializer_class = TvShowSerializer
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='list tvshow general detail [IsAdminOrReadOnly]',
    operation_description='list all tvshow general detail [IsAdminOrReadOnly]', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='create a tvshow general detail [IsAdminOrReadOnly]',
    operation_description='create a tvshow general detail [IsAdminOrReadOnly]', 
))
class TvShowGeneralDetail_LC_View(generics.ListCreateAPIView):
    queryset = TvShowGeneralDetail.objects.all().select_related('tvshow')
    serializer_class = TvshowGeneralDetailSerializer
    permission_classes = [IsAdminOrReadOnly]


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='retrieve particular tvshow general detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='update particular tvshow general detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='patch particular tvshow general detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowGeneralDetail APIs'], operation_id='delete particular tvshow general  detail [IsAdminOrReadOnly]',
))
class TvShowGeneralDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowGeneralDetail.objects.all().select_related('tvshow')
    serializer_class = TvshowGeneralDetailSerializer
    permission_classes = [IsAdminOrReadOnly]






@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='list tvshow core detail [IsAdminOrReadOnly]',
    operation_description='list all tvshow core detail [IsAdminOrReadOnly]', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='create a tvshow core detail [IsAdminOrReadOnly]',
    operation_description='create a tvshow core detail [IsAdminOrReadOnly]', 
))
class TvShowCoreDetail_LC_View(generics.ListCreateAPIView):
    queryset = TvShowCoreDetail.objects.all().select_related('tvshow')
    serializer_class = TvShowCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='retrieve particular tvshow core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='update particular tvshow core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='patch particular tvshow core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowCoreDetail APIs'], operation_id='delete particular tvshow core  detail [IsAdminOrReadOnly]',
))
class TvShowCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowCoreDetail.objects.all().select_related('tvshow')
    serializer_class = TvShowCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]

 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='list tvshow tech specs [IsAdminOrReadOnly]',
    operation_description='list all tvshow tech specs [IsAdminOrReadOnly]', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='create a tvshow tech specs [IsAdminOrReadOnly]',
    operation_description='create a tvshow tech specs [IsAdminOrReadOnly]', 
))
class TvShowTechSpecsDetail_LC_View(generics.ListCreateAPIView):
    queryset = TvShowTechSpecs.objects.all().select_related('tvshow')
    serializer_class = TvShowTechSpecsSerializer
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='retrieve particular tvshow tech specs [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='update particular tvshow tech specs [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='patch particular tvshow tech specs [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowTechSpecs APIs'], operation_id='delete particular tvshow tech specs [IsAdminOrReadOnly]',
))
class TvShowTechSpecsDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowTechSpecs.objects.all().select_related('tvshow')
    serializer_class = TvShowTechSpecsSerializer
    permission_classes = [IsAdminOrReadOnly]

# ----------permission till here

@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='list tvshow rating and review [AllowAny] [Paginate-10]',
    operation_description='list tvshow rating and review [AllowAny]', 
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='create a tvshow rating and review [IsAuthenticated]',
    operation_description='create a tvshow rating and review [IsAuthenticated]', 
))
class TvShowRatingReview_LC_View(generics.ListCreateAPIView):
    queryset = TvShowRatingReview.objects.all().select_related('tvshow')
    serializer_class = TvShowRatingReviewSerializer
    pagination_class = GlobalPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny]
        elif self.request.method == "POST":
            return [permissions.IsAuthenticated]
        return super().get_permissions()


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='retrieve particular tvshow rating and review [IsTVShowReviewer_OrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='update particular tvshow rating and review [IsTVShowReviewer_OrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='patch particular tvshow rating and review [IsTVShowReviewer_OrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App7 : TvShowRatingReview APIs'], operation_id='delete particular tvshow rating and review [IsTVShowReviewer_OrReadOnly]',
))
class TvShowRatingReview_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = TvShowRatingReview.objects.all().select_related('tvshow')
    serializer_class = TvShowRatingReviewSerializer
    permission_classes = [IsTVShowReviewer_OrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserVotes APIs'], operation_id='list all tvshow votes [AllowAny]',
    operation_description='list all tvshow votes [AllowAny]', 
))
class TvShowVotes_List_View(generics.ListAPIView):
    queryset = TvShowVotes.objects.all().select_related('tvshow')
    serializer_class = TvShowVotesSerializer
    

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny]
        elif self.request.method == "POST":
            return [permissions.IsAuthenticated]
        return super().get_permissions()



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserVotes APIs'], operation_id='give vote on tvshow [IsTvShowVoter_OrReadOnly]',
    operation_description='give vote on tvshow [IsTvShowVoter_OrReadOnly]',
)) 
class UserTvShowVotesToggleView(generics.CreateAPIView):
    serializer_class = TvShowVotesSerializer
    permission_classes = [IsTvShowVoter_OrReadOnly]

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
    tags=['App7 : TvShowUserWatchlist APIs'], operation_id='list all user tvshow  watchlist [IsAdminOrUserWatchlistedTvShow]',
    operation_description='list all user tvshow watchlist [IsAdminOrUserWatchlistedTvShow]',
))
class UserTvShowWatchlist_List_View(generics.ListAPIView):
    queryset = UserTvShowWatchlist.objects.all().select_related('tvshow')
    serializer_class = UserTvShowWatchlistSerializer
    permission_classes = [IsAdminOrUserWatchlistedTvShow]
    pagination_class = GlobalPagination 




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserWatchlist APIs'], operation_id='create a user watchlist [IsUserTvShowWatchlist_OrReadOnly]',
    operation_description='create a user watchlist [IsUserTvShowWatchlist_OrReadOnly]',
)) 
class UserTvShowWatchlistToggleView(generics.CreateAPIView):
    serializer_class = UserTvShowWatchlistSerializer
    permission_classes = [IsUserTvShowWatchlist_OrReadOnly]

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
    tags=['App7 : TvShowUserViewed APIs'], operation_id='list all user viewing list [IsAdminOrUserViewedTvShow]',
    operation_description='list all user viewing list [IsAdminOrUserViewedTvShow]',
))
class UserTvShowViewed_List_View(generics.ListAPIView):
    queryset = UserTvShowViewed.objects.all().select_related('tvshow')
    serializer_class = UserTvShowViewedSerializer
    permission_classes = [IsAdminOrUserViewedTvShow]



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShowUserViewed APIs'], operation_id='create a user viewing history [IsUserViewedTvshow_OrReadOnly]',
    operation_description='create a user viewing history [IsUserViewedTvshow_OrReadOnly]',
)) 
class UserTvShowViewedToggleView(generics.CreateAPIView):
    serializer_class = UserTvShowViewedSerializer
    permission_classes = [IsUserViewedTvshow_OrReadOnly]

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




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App7 : TvShow User History APIs'], operation_id='create a user history [IsAuthenticated]',
    operation_description='create a user history [IsAuthenticated]',
)) 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App7 : TvShow User History APIs'], operation_id='create a user history [IsAuthenticated] [Paginate-10]',
    operation_description='create a user history',
)) 
class TvShowWatchHistoryView(generics.ListCreateAPIView):
    queryset = TvShowWatchHistory.objects.all()
    serializer_class = TvShowWatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GlobalPagination
    