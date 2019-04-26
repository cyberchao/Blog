from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('music/', include('music.urls')),
    path('oss/', include('oss.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
#    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
