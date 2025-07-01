# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework import status
# from user_profile.models import UserProfile 
# from django.contrib.auth.models import User

# class TestUserProfileUpdateView(APITestCase):
#     def setUP(self):
#         self.url_profile = reverse('update-profile')
#         self.url_login = reverse('api_token_auth')
#         self.register_payload = {
#             "username" : "testuser",
#             "email" : "testuser@example.com",
#             "password" : "NewPassword@123",
#             "confirm_password" : "NewPassword@123"
#         }
#         self.valid_login_payload= {
#             "username" : "testuser",
#             "password" : "NewPassword@123"
#         }
#         self.user = User.objects.create_user(username='testuser', password='NewPassword@123')


#         # self.profile = self.user.profile # Assuming signal creates profile 

#         # after creating a user it automatically creates the profile


#     def test_update_profile_authenticated(self):
#         response1 = self.client.post(
#             self.url_login , 
#         )
#         # self.client.login(
#         #     username='testuser',
#         #     password='testpass'
#         # )
#         # data = {
#         #     'profile_pic' : 'http://example.com/pic.jpg'
#         # }
#         # response = self.client.patch(self.url, data, format='json')
#         # self.assertEqual(response.status_code, status.HTTP_200_OK)


#         pass


#     def test_update_profile_unauthenticated(self):
#         pass


# # class TestUserProfileInfoView(APITestCase):

# #     def setUP(self):
# #         pass 

# #     def test_get_profile_authenticated(self):
# #         pass

# #     def test_get_profile_unauthenticated(self):
# #         pass

