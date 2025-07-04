from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 

class CastTestCase(APITestCase):

    '''Cast Unit Testing '''
    def setUp(self):
        self.castmedia_data1 = {
            "name": "Hritik Roshan",
            "profile_pics": [
                "https://chatgpt.com/c/6862625f-f870-800f-a200-3b75bf478aeb"
            ],
            "related_pics": [
                "https://chatgpt.com/c/6862625f-f870-800f-a200-3b75bf478aeb"
            ]
        }

        self.castmedia_data2 = {
            "name": "Amir Khan",
            "profile_pics": [
                "https://chatgpt.com/c/6862625f-f870-800f-a200-3b75bf478aeb"
            ],
            "related_pics": [
                "https://chatgpt.com/c/6862625f-f870-800f-a200-3b75bf478aeb"
            ]
        }

        self.cast_data = {
            "castmedia": "Hritik Roshan"
        }

        self.cast_updated_data = {
            "castmedia": "Amir Khan"
        }


    def test_create_cast(self):
        #  create a cast media
        response1 = self.client.post(reverse('cast-media-create'), self.castmedia_data1,format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # create a cast
        response2 = self.client.post(reverse('cast-create-list'), self.cast_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

 

    def test_list_cast(self):
        # create a cast media
        response1 = self.client.post(reverse('cast-media-create'), self.castmedia_data1,format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # create a cast
        response2 = self.client.post(reverse('cast-create-list'), self.cast_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # fetch all cast 
        response2 = self.client.get(reverse('cast-create-list'), self.cast_data, format='json')
        print(response2.data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)



    def test_retireve_particualr_cast(self):
        # create a cast media
        response1 = self.client.post(reverse('cast-media-create'), self.castmedia_data1,format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # create a cast
        response2 = self.client.post(reverse('cast-create-list'), self.cast_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # fetch a particular cast 
        response3 = self.client.get(reverse('cast-detail', kwargs={'pk': 1}), format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)


    def test_update_particular_cast(self):
        # create a cast media
        response1 = self.client.post(reverse('cast-media-create'), self.castmedia_data1,format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.client.post(reverse('cast-media-create'), self.castmedia_data2,format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # create a cast
        response3 = self.client.post(reverse('cast-create-list'), self.cast_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # update a particular cast 
        response3 = self.client.put(reverse('cast-detail', kwargs={'pk': 1}), self.cast_updated_data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)



    def test_delete_particular_cast(self):
        # create a cast media
        response1 = self.client.post(reverse('cast-media-create'), self.castmedia_data1,format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # create a cast
        response2 = self.client.post(reverse('cast-create-list'), self.cast_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # delete a particular cast 
        response3 = self.client.delete(reverse('cast-detail', kwargs={'pk': 1}), format='json')
        self.assertEqual(response3.status_code, status.HTTP_204_NO_CONTENT)

    



class CastCoreDetailTestCase(APITestCase):

    '''Cast Core Detail Unit Testing '''
    def setUp(self):

        self.castmedia_data = {
            "name": "Hritik Roshan",
            "profile_pics": [
                "https://chatgpt.com/c/6862625f-f870-800f-a200-3b75bf478aeb"
            ],
            "related_pics": [
                "https://chatgpt.com/c/6862625f-f870-800f-a200-3b75bf478aeb"
            ]
        }

        self.cast_data ={
            "castmedia": "Hritik Roshan"
        }

        self.cast_core_detail_data = {
            "cast_id": 1,
            "height": "5feet 10inch",
            "born_date": "2025-07-02",
            "death_date": "2025-07-02",
            "spouses": [
                "Shiva"
            ],
            "children": [
                "Hari Krishna"
            ],
            "relatives": [
                "Nice Man"
            ],
            "otherwork": [
                "Good WOrk"
            ]
        }
        

    def test_create_cast_core_detail(self):
        #  create a cast media
        response1 = self.client.post(reverse('cast-media-create'), self.castmedia_data,format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # create a cast
        response2 = self.client.post(reverse('cast-create-list'), self.cast_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # create a cast core detail
        response3 = self.client.post(reverse('cast-core-detail-list-create'), self.cast_core_detail_data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)


    def test_list_cast_core_detail(sefl):
        pass 

    def test_retireve_particualr_cast_core_detail(self):
        pass

    def test_update_particular_cast_core_detail(self):
        pass

    def test_delete_particular_cast_core_detail(self):
        pass
    


