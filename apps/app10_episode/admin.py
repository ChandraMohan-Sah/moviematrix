from django.contrib import admin
from .models import ( 
    Episode, EpisodeGeneralDetail, EpisodeWatchlist,
    EpisodeViewed, EpisodeVotes, EpisodeRatingReview
)


# Register your models here.
admin.site.register(Episode)
admin.site.register(EpisodeGeneralDetail)
admin.site.register(EpisodeWatchlist)
admin.site.register(EpisodeViewed)
admin.site.register(EpisodeVotes)
admin.site.register(EpisodeRatingReview)
 