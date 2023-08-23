from django.urls import include, path

from api_core.views import SchemaView

urlpatterns = [
    path('', include('api_auth.urls')),
    path('docs<format>/', SchemaView.without_ui(cache_timeout=0), name='schema_json'),
    path('docs/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('redocs/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema_redoc'),
]
