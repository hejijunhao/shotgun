# shotgun/urls.py
from django.contrib import admin
from django.urls import path, include  # Import 'include' to link to app-level URLs

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('', include('reservations.urls')),  # Include the reservations app's URLs
]