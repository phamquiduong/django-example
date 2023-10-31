from django.urls import path

from apps.authentication.views import api_views

urlpatterns = [
    path('csrf', api_views.get_csrf_token_view, name='Authentication API Get CSRF Token'),

    path('register', api_views.register_view, name='Authentication API Register'),

    path('login', api_views.login_view, name='Authentication API Login'),
    path('refresh', api_views.refresh_token_view, name='Authentication API Refresh Token'),

    path('user', api_views.get_user_info_view, name='Authentication API Get User Info'),
]
