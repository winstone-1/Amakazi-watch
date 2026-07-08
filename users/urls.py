from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import RegisterView, CustomTokenObtainPairView, GoogleAuthCallbackView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/callback/', GoogleAuthCallbackView.as_view(), name='google-callback'),
]
