from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import CustomUser


class Car(models.Model):
    """Car listing model."""
    
    FUEL_TYPE_CHOICES = (
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('delisted', 'Delisted'),
    )
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cars')
    title = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(validators=[
        MinValueValidator(1900),
        MaxValueValidator(2100)
    ])
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    
    # Car specs
    mileage = models.IntegerField(help_text="Mileage in kilometers")
    transmission = models.CharField(max_length=50, choices=[('manual', 'Manual'), ('automatic', 'Automatic')])
    seats = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    color = models.CharField(max_length=50)
    
    # Documents
    rc_document = models.FileField(upload_to='car_documents/rc/')
    insurance_document = models.FileField(upload_to='car_documents/insurance/', null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_available = models.BooleanField(default=True)
    
    # Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_bookings = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete
    
    class Meta:
        db_table = 'car'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['location', 'price_per_day']),
            models.Index(fields=['fuel_type']),
            models.Index(fields=['is_available']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"


class CarImage(models.Model):
    """Multiple images for a car listing."""
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'car_image'
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"Image for {self.car}"


class Review(models.Model):
    """Reviews for cars."""
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='car_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review'
        ordering = ['-created_at']
        unique_together = ['car', 'reviewer']  # One review per car per user
    
    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.car}"
