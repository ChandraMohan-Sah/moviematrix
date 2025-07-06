from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class TestCreate_CastMedia(APITestCase):

    def setUp(self):
        self.cast_media_url = reverse('cast-media-create')
        self.register_url = reverse('registration_view')

        # Create admin and normal users
        self.admin_user, self.admin_token = self._register_user_and_get_token(is_admin=True, username="adminuser")
        self.normal_user, self.normal_token = self._register_user_and_get_token(is_admin=False, username="normaluser")
        
        # Validated Data
        self.cast_validated_data = {
            "name": "Ram Joshi Cast",
            "profile_pics": [
                "https://plus.unsplash.com/premium_photo-1747054587747-bd631e58c312"
            ],
            "related_pics": [
                "https://plus.unsplash.com/premium_photo-1747054587747-bd631e58c312"
            ]
        }


    def _register_user_and_get_token(self, is_admin=False, username="testuser"):
        """Register a user using the registration API and return user and token"""
        user_data = {
            "username": username,
            "email": f"{username}@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123"
        }

        # Register user
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        user.is_staff = is_admin
        user.save()

        # Get token
        token = Token.objects.get(user=user)
        return user, token


    def test_admin_can_create_castmedia(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.post(self.cast_media_url, self.cast_validated_data, format='json')
        print("CastMedia creation response:", response.data)  # <-- Add this line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_non_admin_cannot_create_castmedia(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.normal_token.key}")
        response = self.client.post(self.cast_media_url, self.cast_validated_data, format='json')
        print("CastMedia creation response: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class TestCreate_CreatorMedia(APITestCase):

    def setUp(self):
        self.creator_media_url = reverse('creator-media-create')
        self.register_url = reverse('registration_view')

        # create admin and normal users 
        self.admin_user, self.admin_token = self._register_user_and_get_token(is_admin=True, username='adminuser')
        self.normal_user, self.normal_token = self._register_user_and_get_token(is_admin=False, username="normaluser")

        # validated data 
        self.creator_validated_data = {
            "name": "Ram Joshi Creator",
            "profile_pics": [
                "https://plus.unsplash.com/premium_photo-1747054587747-bd631e58c312"
            ],
            "related_pics": [
                "https://plus.unsplash.com/premium_photo-1747054587747-bd631e58c312"
            ]
        }


    def _register_user_and_get_token(self, is_admin=False, username="testuser"):
        """Register a user using the registration API and return user and token"""
        user_data = {
            "username": username,
            "email": f"{username}@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123"
        }

        # Register user
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        user.is_staff = is_admin
        user.save()

        # Get token
        token = Token.objects.get(user=user)
        return user, token


    def test_admin_can_create_creatormedia(self):
        self.client.credentials(HTTP_AUTHORIZATION= f"Token {self.admin_token.key}")
        response = self.client.post(self.creator_media_url, self.creator_validated_data, format='json')
        print("CreatorMedia Creation response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_non_admin_cannot_create_creatormedia(self):
        self.client.credentials(HTTP_AUTHORIZATION= f"Token {self.normal_token.key}")
        response = self.client.post(self.creator_media_url, self.creator_validated_data, format='json')
        print("CreatorMedia Creation response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

     


class TestCreate_WriterMedia(APITestCase):

    def setUp(self):
        self.writer_media_url = reverse('writer-media-create')
        self.register_url = reverse('registration_view')

        # create admin and normal users 
        self.admin_user, self.admin_token = self._register_user_and_get_token(is_admin=True, username="adminuser")
        self.normal_user, self.normal_token = self._register_user_and_get_token(is_admin=False, username="normaluser")

        #validated data 
        self.writer_validated_data = {
            "name": "Ram Joshi Writer",
            "profile_pics": [
                "https://plus.unsplash.com/premium_photo-1747054587747-bd631e58c312"
            ],
            "related_pics": [
                "https://plus.unsplash.com/premium_photo-1747054587747-bd631e58c312"
            ]       
        }

    def _register_user_and_get_token(self, is_admin=False, username="testuser"):
        user_data = {
            "username" : username,
            "email" : f"{username}@example.com",
            "password":"testpass123",
            "confirm_password":"testpass123"
        }

        #register user 
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        user.is_staff = is_admin 
        user.save() 
        
        # Get Token 
        token = Token.objects.get(user=user)
        return user, token 
    

    def test_admin_can_create_writermedia(self):
        self.client.credentials(HTTP_AUTHORIZATION= f"Token {self.admin_token.key}")
        response = self.client.post(self.writer_media_url, self.writer_validated_data, format='json' )
        print("WriterMedia Creation Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_create_writermedia(self):
        self.client.credentials(HTTP_AUTHORIZATION= f"Token {self.normal_token.key}")
        response = self.client.post(self.writer_media_url, self.writer_validated_data, format='json' )
        print("WriterMedia Creation Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    


class TestCreate_MovieMedia(APITestCase):

    def setUp(self):
        self.movie_media_url = reverse('movie-media-create')
        self.register_url = reverse('registration_view')

        # create admin and normal users 
        self.admin_user, self.admin_token = self._register_user_and_get_token(is_admin=True, username='adminuser')
        self.normal_user, self.normal_token = self._register_user_and_get_token(is_admin=False, username="normaluser")

        # validated data 
        self.movie_validated_data = {
            "name": "Nadiya Ka Paar",
            "banners": [
                "http://example.com"
            ],
            "thumbnails": [
                "http://example.com"
            ],
            "trailers": [
                "http://example.com"
            ],
            "videos": [
                "http://example.com"
            ],
            "related_pics": [
                "http://example.com"
            ]
        }


    def _register_user_and_get_token(self, is_admin=False, username="testuser"):
        """Register a user using the registration API and return user and token"""
        user_data = {
            "username": username,
            "email": f"{username}@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123"
        }

        # Register user
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        user.is_staff = is_admin
        user.save()

        # Get token
        token = Token.objects.get(user=user)
        return user, token


    def test_admin_can_create_moviemedia(self):
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {self.admin_token.key}")
        response = self.client.post(self.movie_media_url, self.movie_validated_data, format='json')
        print("MovieMedia Creation Response : ", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



