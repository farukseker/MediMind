from django.urls import path, include
from .views import CustomTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "auth"

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='register')
]
