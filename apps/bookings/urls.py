from django.urls import path
from apps.bookings import views

urlpatterns = [
    path('create/<int:car_id>/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
