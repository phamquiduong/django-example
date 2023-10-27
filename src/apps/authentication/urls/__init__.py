from django.urls import include, path

urlpatterns = [
    path('api/', include('apps.authentication.urls.api_urls'), name='Authentication API')
]
