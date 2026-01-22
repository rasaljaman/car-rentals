from rest_framework import serializers
from apps.cars.models import Car, CarImage, Review


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'is_primary', 'created_at']
        read_only_fields = ['created_at']


class CarListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = ['id', 'title', 'brand', 'model', 'year', 'fuel_type', 'price_per_day',
                 'location', 'rating', 'owner_name', 'status', 'is_available', 'primary_image', 'created_at']
        read_only_fields = ['id', 'rating', 'status', 'created_at']
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return CarImageSerializer(primary).data
        return None


class CarDetailSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Car
        fields = ['id', 'title', 'brand', 'model', 'year', 'fuel_type', 'price_per_day',
                 'location', 'description', 'registration_number', 'mileage', 'transmission',
                 'seats', 'color', 'status', 'is_available', 'rating', 'total_bookings',
                 'owner', 'images', 'created_at']
        read_only_fields = ['id', 'rating', 'total_bookings', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'reviewer_name', 'created_at']
        read_only_fields = ['id', 'created_at']
