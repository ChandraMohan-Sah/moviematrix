from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 
from django.contrib.auth import get_user_model


# ------------ General Movie Information --------
class Movie_TestCase(APITestCase):

    def setUp(self):
         # ✅ Create and authenticate admin user
        self.admin_user = get_user_model().objects.create_user(
            username='admin', password='admin123', is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

        self.moviemedia_creation_url = reverse('movie-media-create')
        self.castmedia_creation_url = reverse('cast-media-create')
        self.creatormedia_creation_url = reverse('creator-media-create')
        self.writermedia_creation_url = reverse('writer-media-create')

        self.genre_creation_url = reverse('genre-list-create')
        self.platform_creation_url = reverse('platform-list-create')
        self.cast_creation_url = reverse('cast-create-list')
        self.creator_creation_url = reverse('creator-list-create')
        self.writer_creation_url = reverse("writer-list-create")

        self.movie_creation_url = reverse('movie-list-create')

        self.moviemedia_data = {
            "name": "Nadiya Ka Paar",
            "banners": [
                "https://example.com/banner.jpg"
            ],
            "thumbnails": [
                "https://example.com/thumb.jpg"
            ],
            "trailers": [
                "https://example.com/trailer.mp4"
            ],
            "videos": [
                "https://example.com/video.mp4"
            ],
            "related_pics": [
                "https://example.com/related.jpg"
            ]
        }

        self.castmedia_data = {
            "name": "Hritik Roshan",
            "profile_pics": [
                "https://example.com/hritik-profile.jpg"
            ],
            "related_pics": [
                "https://example.com/hritik-related.jpg"
            ]
        }

        self.creatormedia_data = {
            "name": "Radha Krishna",
            "profile_pics": [
                "https://example.com/krishna-profile.jpg"
            ],
            "related_pics": [
                "https://example.com/krishna-related.jpg"
            ]
        }

        self.writermedia_data = {
            "name": "ROshan the Writer",
            "profile_pics": [
                "https://example.com/writer-profile.jpg"
            ],
            "related_pics": [
                "https://example.com/writer-related.jpg"
            ]
        }

        self.genre_data = {
            "name": "Hari Bahadur"
        }

        self.platform_data = {
            "platform": "Netflix"
        }

    def test_create_movie(self):
        # Create Media Entries
        movie_media_res = self.client.post(self.moviemedia_creation_url, self.moviemedia_data, format='json')
        self.assertEqual(movie_media_res.status_code, status.HTTP_201_CREATED)
        moviemedia_slug = movie_media_res.data['movie_slug']
        print(f"✅ MovieMedia created with ID: {moviemedia_slug}")

        cast_media_res = self.client.post(self.castmedia_creation_url, self.castmedia_data, format='json')
        self.assertEqual(cast_media_res.status_code, status.HTTP_201_CREATED)
        castmedia_id = cast_media_res.data['id']
        print(f"✅ CastMedia created with ID: {castmedia_id}")

        creator_media_res = self.client.post(self.creatormedia_creation_url, self.creatormedia_data, format='json')
        self.assertEqual(creator_media_res.status_code, status.HTTP_201_CREATED)
        creatormedia_id = creator_media_res.data['id']
        print(f"✅ CreatorMedia created with ID: {creatormedia_id}")

        writer_media_res = self.client.post(self.writermedia_creation_url, self.writermedia_data, format='json')
        self.assertEqual(writer_media_res.status_code, status.HTTP_201_CREATED)
        writermedia_id = writer_media_res.data['id']
        print(f"✅ WriterMedia created with ID: {writermedia_id}")

        # Create Platform and Genre
        platform_res = self.client.post(self.platform_creation_url, self.platform_data, format='json')
        self.assertEqual(platform_res.status_code, status.HTTP_201_CREATED)
        platform_id = platform_res.data['id']
        print(f"✅ Platform created with ID: {platform_id}")

        genre_res = self.client.post(self.genre_creation_url, self.genre_data, format='json')
        self.assertEqual(genre_res.status_code, status.HTTP_201_CREATED)
        genre_id = genre_res.data['id']
        print(f"✅ Genre created with ID: {genre_id}")

        # Create Cast, Creator, Writer entries
        cast_res = self.client.post(self.cast_creation_url, {"castmedia": self.castmedia_data["name"]}, format='json')
        self.assertEqual(cast_res.status_code, status.HTTP_201_CREATED)
        cast_id = cast_res.data['id']
        print(f"✅ Cast created with ID: {cast_id}")

        creator_res = self.client.post(self.creator_creation_url, {"creatormedia": self.creatormedia_data["name"]}, format='json')
        self.assertEqual(creator_res.status_code, status.HTTP_201_CREATED)
        creator_id = creator_res.data['id']
        print(f"✅ Creator created with ID: {creator_id}")

        writer_res = self.client.post(self.writer_creation_url, {"writermedia": self.writermedia_data["name"]}, format='json')
        self.assertEqual(writer_res.status_code, status.HTTP_201_CREATED)
        writer_id = writer_res.data['id']
        print(f"✅ Writer created with ID: {writer_id}")

        # Now preparing final movie data using dynamic IDs
        movie_data = {
            "moviemedia": moviemedia_slug,  
            "movie_genre_ids": [genre_id],
            "platform_id": platform_id,
            "movie_cast_ids": [cast_id],
            "movie_creator_ids": [creator_id],
            "movie_writer_ids": [writer_id]
        }

        movie_res = self.client.post(self.movie_creation_url, movie_data, format='json')
        print("Movie creation response:", movie_res.data)
        print("Status Code:", movie_res.status_code)
        self.assertEqual(movie_res.status_code, status.HTTP_201_CREATED)


    def test_get_all_movie(self):
        pass 

    def test_retrieve_particular_movie(self):
        pass 

    def test_update_particular_movie(self):
        pass 

    def test_partial_update_particular_movie(self):
        pass 

    def test_delete_particular_movie(self):
        pass 



# ------------- Movie Details -------------------

class MovieGeneralDetail_TestCase(APITestCase):
    pass

class MovieCoreDetail_TestCase(APITestCase):
    pass

class MovieBoxOffice_TestCase(APITestCase):
    pass

class MovieTechSpecs_TestCase(APITestCase):
    pass



# ------------- user specific  -------------------


class MovieRatingReview_TestCase(APITestCase):
    pass


class UserMovieWatchlist_TestCase(APITestCase):
    pass

class UserMovieViewed_TestCase(APITestCase):
    pass

class MovieVotes_TestCase(APITestCase):
    pass

class MovieWatchHistory_TestCase(APITestCase):
    pass


# ---------------------------------------------------