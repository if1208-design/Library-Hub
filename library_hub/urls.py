from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from library import views  # ← ADD THIS IMPORT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),  # This includes all library URLs
    path('cart/', views.cart, name='cart'),
]

# Serve static/media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)