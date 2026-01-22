from rest_framework import serializers
from apps.accounts.models import CustomUser, Profile, OTPVerification


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'location',
                 'is_verified', 'is_email_verified', 'is_phone_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified', 'is_email_verified', 'is_phone_verified']


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'profile_photo', 'bio', 'rating', 'total_reviews', 'total_rentals', 'total_listings']
        read_only_fields = ['rating', 'total_reviews', 'total_rentals', 'total_listings']


class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = ['id', 'otp_type', 'is_verified', 'expires_at']
        read_only_fields = ['id', 'expires_at']
