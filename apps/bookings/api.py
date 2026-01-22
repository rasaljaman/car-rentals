from rest_framework import serializers
from apps.bookings.models import Booking, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    car_title = serializers.CharField(source='car.title', read_only=True)
    renter_name = serializers.CharField(source='renter.get_full_name', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'car', 'car_title', 'renter', 'renter_name', 'owner', 'owner_name',
                 'start_date', 'end_date', 'total_days', 'price_per_day', 'total_price',
                 'status', 'payment', 'created_at']
        read_only_fields = ['id', 'total_days', 'total_price', 'created_at']
