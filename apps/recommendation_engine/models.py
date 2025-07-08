from django.db import models


 
'''
    1. Fetch all movie preferences (watched, rated, etc.)
    2. Exclude those from the full movie set
    3. Score unseen movies based on matching genres, directors, or casts from watched/rated ones
    4. Return top recommended movies
'''

'''Personalized Movie Recommendation'''
def personalized_movie_recommendation(user_id):
    # fetch all data from : users_movie_preferences
    # then Filters + ranks unseen movies based on preferences
    # filter based on ()
    pass


'''Personalized Tvshow Recommendataion '''
def personalized_tvshow_recommendation(user_id):
    # fetch all data from : users_tvshow_preferences
    # then Filters + ranks unseen tvshows based on preferences
    # filter based on ()
    pass


'''Personalized stars Recommendataion '''
def personalized_stars_recommendation(user_id):
    # fetch all data from : users_stars_preferences
    # then Filters + ranks unseen stars based on preferences
    # filter based on ()
    pass

