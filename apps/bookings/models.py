from django.db import models
from apps.accounts.models import CustomUser
from apps.cars.models import Car


class Booking(models.Model):
    """Booking/Rental request model."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active Rental'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    renter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_as_renter')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_as_owner')
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Pricing
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    total_days = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Additional info
    pickup_location = models.CharField(max_length=255, blank=True)
    dropoff_location = models.CharField(max_length=255, blank=True)
    renter_notes = models.TextField(blank=True)
    owner_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'booking'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['renter', 'status']),
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['car', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"Booking #{self.id} - {self.car} by {self.renter.email}"


class Payment(models.Model):
    """Payment model for bookings."""
    
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('wallet', 'Wallet'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, unique=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"
