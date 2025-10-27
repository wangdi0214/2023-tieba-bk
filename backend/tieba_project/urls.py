"""tieba_project URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user_app.urls')),
    path('api/tieba/', include('tieba_app.urls')),
    path('api/posts/', include('post_app.urls')),
    path('api/comments/', include('comment_app.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)