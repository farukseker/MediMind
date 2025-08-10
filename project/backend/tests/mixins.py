from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User


class JWTAuthTestMixin:
    def create_user(self, username='echo', password='echo12345!'):
        return User.objects.create_user(username=username, password=password)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get_authenticated_client(self, user):
        token = self.get_token_for_user(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return client

"""
# Example test > 
class MyTest(APITestCase, JWTAuthTestMixin):
    def setUp(self):
        self.user1 = self.create_user(username='user1')
        self.user2 = self.create_user(username='user2')

        self.client1 = self.get_authenticated_client(self.user1)
        self.client2 = self.get_authenticated_client(self.user2)
"""