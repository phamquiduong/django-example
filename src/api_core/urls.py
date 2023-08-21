from django.urls import include, path

from .views import schema_view

urlpatterns = [
    path('', include('api_auth.urls')),
    path('docs<format>/', schema_view.without_ui(cache_timeout=0), name='schema_json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema_redoc'),
]
