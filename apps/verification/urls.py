from django.urls import path
from apps.verification import views

urlpatterns = [
    path('upload/', views.upload_verification, name='upload_verification'),
    path('status/', views.verification_status, name='verification_status'),
    path('approve/<int:user_id>/', views.approve_user_verification, name='approve_user_verification'),
]
