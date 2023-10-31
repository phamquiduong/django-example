from django.urls import path

from apps.authentication.views import api_views

urlpatterns = [
    path('csrf', api_views.get_csrf_token, name='Authentication API Get CSRF Token'),

    path('login', api_views.login, name='Authentication API Login'),
    path('refresh', api_views.refresh_token, name='Authentication API Refresh Token'),

    path('user', api_views.get_user_info, name='Authentication API Get User Info'),
]
