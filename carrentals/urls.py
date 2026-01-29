"""
URL configuration for Sura Rentals project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('apps.admin_panel.urls')),
    path('', include('apps.accounts.urls')),
    path('cars/', include('apps.cars.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('verify/', include('apps.verification.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
