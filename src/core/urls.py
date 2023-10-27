from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import RedirectView

urlpatterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(
        url='https://static.djangoproject.com/img/icon-touch.e4872c4da341.png', permanent=True)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
