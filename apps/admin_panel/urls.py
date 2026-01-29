from django.urls import path
from apps.admin_panel import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-car/', views.admin_add_car, name='admin_add_car'),
    path('approve-car/<int:car_id>/', views.admin_approve_car, name='admin_approve_car'),
    path('reject-car/<int:car_id>/', views.admin_reject_car, name='admin_reject_car'),
    path('delete-car/<int:car_id>/', views.admin_delete_car, name='admin_delete_car'),
    path('users/', views.admin_view_users, name='admin_view_users'),
]
