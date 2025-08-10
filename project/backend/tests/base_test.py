from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
# from django.contrib.auth.models import User
from custom_auth.models import  User

class BaseAPITestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def _create_user_and_get_token(self, email, password='testpassword123!'):
        user = User.objects.create_user(email=email, password=password)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return user, access_token

    def _authenticate_client(self, access_token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

"""
# Example usage
from tests.base_test import BaseAPITestCase  

class MultiUserFavoritesTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        
        self.user1, self.token1 = self._create_user_and_get_token(username='user1')
        self.user2, self.token2 = self._create_user_and_get_token(username='user2')

"""