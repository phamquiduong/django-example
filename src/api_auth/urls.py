from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views.user_view import CreateUserView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='api_register'),

    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='api_verify'),
]
