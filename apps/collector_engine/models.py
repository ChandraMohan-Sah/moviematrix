from django.db import models

# Background task using celery  + paginate 10 

# ----------Collaborative + Content Based Filtering --------------

'''Popular Celebrity|Cast'''
# collect - fetch cast of (movie, tvshow) with maximum rating


'''Fan Favourites'''
# collect - movies with top ratings
# collect - movies with most number of  votes


'''Popular Movies'''
# collect - movie with maximum reviews 


'''IMDB Originals'''
# collect - is_original=True (random function )


'''Prime Video'''
# collect platform = prime (random function)


'''In Theaters'''
# collect by release date <= today <= release_date + 8 weeks (random function)


'''Coming Soon to Theaters + Editors Picks'''
# collect : release_date > today (random function)


'''Your May Like '''
# collect user specific


'''Recently Viewed : Watch History '''
# collect user specific 



 
# ---------Page Wise Collection ------------------------

''' For Movie Page '''
def collect_featured_movies():
    # one recent movie with maximum rating
    # one recent movie with maximum likes
    pass


''' For Tvshow Page '''
def collect_featured_tvshow():
    # one recent tvshow with maximum rating 
    # one recent tvshow with maximum likes
    pass


''' For Episode Page '''
def collect_featured_episode():
    # one recent episode with maximum rating 
    # one recent episode with maximum likes 
    pass


''' For Home Page'''
def collect_featured_home():
    # one recent movie with maximum rating
    # one recent movie with maximum likes
    # one recent tvshow with maximum rating 
    # one recent tvshow with maximum likes
    # one recent episode with maximum rating 
    # one recent episode with maximum likes 
    pass

# -----------------------------------------------------

