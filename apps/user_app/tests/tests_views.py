from rest_framework import status
from rest_framework.test import APITestCase 
from rest_framework.authtoken.models import Token 

from django.contrib.auth.models import User
from django.urls import reverse


'''
    Tips:
        - Test what should work
        - Test what should not work
        - Test for side effects (e.g. user/token creation)

        
    Notes : 
        - setUp() method                                                
                : organizes test data cleanly. Reusable

        - assertEqual(response.status_code, status.HTTP_201_CREATED)	
                : verifies the status code.
                : fails if the status code is not 201

        - assertIn("token", response.data)	                            
                : verifies if the response has a key named "token" or not
                : doen't care what the value of token is.

        - assertEqual(response.data["username"], "testuser")	
                : Verifies if the response has a key named "username" or not
                : also verifies if the value of the key "username" is exactly "testuser" or not
                : fails if the key is missing or value is different 

'''
 

class TestRegisterationView(APITestCase):

    def setUp(self):
        self.url = reverse('registration_view')
        self.valid_payload = {
            "username" : "testcase",
            "email" : "testcase@example.com",
            "password" : "NewPassword@123",
            "confirm_password" : "NewPassword@123"
        }

        self.invalid_payload = {
            "username" : "testcase",
            "email" : "testcase@example.com",
            "password" : "NewPassword@123",
            "confirm_password" : "NewPassword@1234"
        }

    def test_registeration_success(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        # variuos checks
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)                          
        self.assertIn("token", response.data)
        self.assertTrue(User.objects.filter(username="testuser").exists)


    def test_registration_failure(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        # various checks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password do not match", str(response.data))
        


class TestLoginView(APITestCase):

    def setUp(self):
        self.url_register = reverse('registration_view')
        self.url_login = reverse('api_token_auth')
        self.register_payload = {
            "username" : "testuser",
            "email" : "testuser@example.com",
            "password" : "NewPassword@123",
            "confirm_password" : "NewPassword@123"
        }
        self.valid_login_payload= {
            "username" : "testuser",
            "password" : "NewPassword@123"
        }

        self.invalid_login_payload = {
            "username" : "testuser",
            "password" : "NewPassword@1234"
        }


    def test_register_then_login_success(self):
        response1 = self.client.post(self.url_register, self.register_payload, format='json')
        response2 = self.client.post(self.url_login, self.valid_login_payload, format='json')
        # various 
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertIn("token", response2.data)
        self.assertTrue(User.objects.filter(username="testuser").exists)


    def test_register_then_login_filure(self):
        response1 = self.client.post(self.url_register, self.register_payload, format='json')
        response2 = self.client.post(self.url_login, self.invalid_login_payload, format='json')
        # various checks
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)



class TestLogoutView(APITestCase):
    def setUp(self):
        self.url_register = reverse('registration_view')
        self.url_login = reverse('api_token_auth')
        self.url_logout = reverse('logout')
        self.register_payload = {
            "username" : "testuser",
            "email" : "testuser@example.com",
            "password" : "NewPassword@123",
            "confirm_password" : "NewPassword@123"
        }
        self.login_payload = {
            "username" : "testuser",
            "password" : "NewPassword@123"
        }
        self.logout_payload = {
            "username" : "testuser",
            "password" : "NewPassword@123"
        }


    def test_logout_success(self):
        response1 = self.client.post(self.url_register, self.register_payload, format='json')
        response2 = self.client.post(self.url_login, self.login_payload, format='json')
        # fetch token after login
        token = response2.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response3 = self.client.post(self.url_logout, {}, format='json')

        # various checks
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK) 
        self.assertEqual(response3.status_code, status.HTTP_200_OK) 
        self.assertIn("Logout Successfully", str(response3.data)) 








'''
I used APITestCase for testing the API endpoints.
All the necessary methds that it contains are :
    1. self.client.get()
    2. self.client.post()
    3. self.client.put()
    4. self.client.patch()
    5. self.client.delete()

    6. self.client.head()
    7. self.client.options()
    8. self.client.trace()

    9. self.client.login()
    10. self.client.logout()
    11. self.client.force_authenticate()
    12. self.client.credentials()

    13. self.client.request()
    14. self.client.generic()

    15. self.client.assertContains()
    16. self.client.assertNotContains()

    17. self.client.assertRedirects()

    20. self.client.assertFormError()
    21. self.client.assertFormSetError()
    22. self.client.assertQuerysetEqual()
    23. self.client.assertNumQueries()
    24. self.client.assertJSONEqual()
    25. self.client.assertJSONNotEqual()

    30. self.client.assertURLEqual()
    31. self.client.assertURINotEqual()

    32. self.assertEqual()
    33. self.assertNotEqual()
    34. self.assertTrue()
    35. self.assertFalse()
    36. self.assertIs()
    37. self.assertIsNot()
    38. self.assertIsNone()
    39. self.assertIsNotNone()
    40. self.assertIn()
    41. self.assertNotIn()
    42. self.assertIsInstance()
    43. self.assertNotIsInstance()

'''

