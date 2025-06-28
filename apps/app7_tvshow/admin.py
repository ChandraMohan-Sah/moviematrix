from django.contrib import admin
from .models import (
    TvShow, TvShowGeneralDetail,
    TvShowCoreDetail, TvShowTechSpecs,
    UserTvShowWatchlist, UserTvShowViewed, TvShowVotes,
    TvShowRatingReview
)

# Register your models here.

admin.site.register(TvShow)
admin.site.register(TvShowGeneralDetail)
admin.site.register(TvShowCoreDetail)
admin.site.register(TvShowTechSpecs)
admin.site.register(UserTvShowWatchlist)
admin.site.register(UserTvShowViewed)
admin.site.register(TvShowVotes)
admin.site.register(TvShowRatingReview)
