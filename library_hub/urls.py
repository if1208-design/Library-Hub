from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),         # Handles dashboard, books catalogue, and API data layers
    path('', include('authentication.urls')),  # Handles login, signup, and account recoveries
]

# Serve static/media files in development mode (Ensures your custom CSS/JS assets load smoothly)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)