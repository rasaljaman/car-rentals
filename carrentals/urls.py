"""
URL configuration for Sura Rentals project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views
from apps.core import views as core_views
from apps.cars import views as car_views


urlpatterns = [
    path("control-panel-9xA7/", core_views.admin_login),
    path("admin-dashboard/", core_views.admin_dashboard),
    path("admin/add-car/", car_views.admin_add_car),
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
