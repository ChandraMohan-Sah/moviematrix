from django.contrib import admin
from .models import (
        Movie, MovieGeneralDetail , MovieRatingReview,  MovieCoreDetail, MovieBoxOffice,
        MovieTechSpecs, UserMovieWatchlist, UserMovieViewed, MovieVotes
    )


admin.site.register(Movie)
admin.site.register(MovieGeneralDetail)
admin.site.register(MovieRatingReview)
admin.site.register(MovieCoreDetail)
admin.site.register(MovieBoxOffice)
admin.site.register(MovieTechSpecs)
admin.site.register(UserMovieWatchlist)
admin.site.register(UserMovieViewed)
admin.site.register(MovieVotes)

