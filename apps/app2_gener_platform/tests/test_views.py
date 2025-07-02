from rest_framework.test import APITestCase 
from rest_framework import status
from django.urls import reverse
# from app2_gener_platform.models import Genre, Platform 


class GenerPlatformTestCase(APITestCase):

    '''Genre Unit Testing '''
    def test_create_genre(self):
        data = {
            "name": "Action"
        }
        response = self.client.post(reverse('genre-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_list_genre(self):
        data = {
            "name": "Romance"
        }
        # create a genre
        response1 = self.client.post(reverse('genre-list'), data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # fetch all genre
        response2 = self.client.get(reverse('genre-list'), format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)



    def test_get_particular_genre_detail(self):
        data1 = {
            "name": "Thriller"
        }
        data2 = {
            "name": "Horror"
        }
        # create a genre
        response1 = self.client.post(reverse('genre-list'), data1, format='json')
        response1 = self.client.post(reverse('genre-list'), data2, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # fetch particular genre
        response2 = self.client.get(reverse('genre-detail', kwargs={'pk':2}), format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        

    def test_update_particular_genre(self): 
        data = {
            "name": "Comedy"
        }
        updated_data = {
            "name": "Drama"
        }
        # create a genre 
        response = self.client.post(reverse('genre-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update a genre
        response = self.client.put(reverse('genre-detail', kwargs={'pk':1}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_partial_update_genre(self):
        data = {
            "name": "Comedy"
        }
        updated_data = {
            "name": "Drama"
        }
        # create a genre 
        response = self.client.post(reverse('genre-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update a genre
        response = self.client.patch(reverse('genre-detail', kwargs={'pk':1}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_genre(self):
        data = {
            "name": "Comedy"
        }
        # create a genre 
        response = self.client.post(reverse('genre-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # delete a genre
        response = self.client.delete(reverse('genre-detail', kwargs={'pk':1}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
   
    

class PlatformTestCase(APITestCase):
    '''Platform Unit Testing '''
    def test_create_platform(self):
        data = {
            "platform" : "Amazon Prime"
        }
        
        response = self.client.post(reverse('platform-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_list_platform(self):
        data = {
            "platform" : "Amazon Prime"
        }
        # create a platform
        response1 = self.client.post(reverse('platform-list'), data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # fetch all platform
        response2 = self.client.get(reverse('platform-list'), format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        

    def test_get_particular_platform_detail(self):
        data = {
            "platform" : "Amazon Prime"
        }
        # create a platform
        response1 = self.client.post(reverse('platform-list'), data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # fetch particular platform
        response2 = self.client.get(reverse('platform-detail', kwargs={'pk':1}), format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


    def test_update_particular_platform(self):
        data = {
            "platform" : "Amazon Prime"
        }
        updated_data = {
            "platform" : "Netflix"
        }
        # create a platform
        response1 = self.client.post(reverse('platform-list'), data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # update a platform
        response2 = self.client.put(reverse('platform-detail', kwargs={'pk':1}), updated_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        

    def test_partial_update_platform(self):
        data = {
            "platform" : "Amazon Prime"
        }
        updated_data = {
            "platform" : "Netflix"
        }
        # create a platform
        response1 = self.client.post(reverse('platform-list'), data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # update a platform
        response2 = self.client.patch(reverse('platform-detail', kwargs={'pk':1}), updated_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

      

    def test_delete_platform(self):
        data = {
            "platform" : "Amazon Prime"
        }
        # create a platform
        response1 = self.client.post(reverse('platform-list'), data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # delete a platform
        response2 = self.client.delete(reverse('platform-detail', kwargs={'pk':1}), format='json')
        
