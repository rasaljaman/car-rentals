from django.urls import path
from apps.cars import views

urlpatterns = [
    path('browse/', views.browse_cars, name='browse_cars'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),
    path('create/', views.create_car_listing, name='create_car_listing'),
    path('<int:car_id>/edit/', views.edit_car_listing, name='edit_car_listing'),
    path('<int:car_id>/delete/', views.delete_car_listing, name='delete_car_listing'),
    path('<int:car_id>/review/', views.add_car_review, name='add_car_review'),
]
