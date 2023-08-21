from django.urls import include, path

urlpatterns = [
    path('', include('api_auth.urls'))
]
