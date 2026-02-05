from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import CustomUser


class Car(models.Model):
    """Car listing model."""

    FUEL_TYPE_CHOICES = (
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("electric", "Electric"),
        ("hybrid", "Hybrid"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending Verification"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
        ("delisted", "Delisted"),
    )

    TRANSMISSION_CHOICES = (
        ("manual", "Manual"),
        ("automatic", "Automatic"),
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cars",
        null=True,
        blank=True,  # Admin-added cars
    )

    # Basic info
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )

    # Pricing & location
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    location = models.CharField(max_length=255)

    # Specs
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(
        max_length=20, choices=TRANSMISSION_CHOICES
    )
    seats = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    mileage = models.IntegerField(help_text="Mileage in kilometers")
    color = models.CharField(max_length=50)

    # Registration
    registration_number = models.CharField(
        max_length=50, unique=True
    )

    # Documents (Supabase URLs)
    rc_document_url = models.URLField()
    insurance_document_url = models.URLField(blank=True, null=True)

    # Status & stats
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0
    )
    total_bookings = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "car"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["location", "price_per_day"]),
            models.Index(fields=["fuel_type"]),
            models.Index(fields=["is_available"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"


class CarImage(models.Model):
    """Multiple images for a car (Supabase Storage)."""

    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="images"
    )
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "car_image"
        ordering = ["-is_primary", "created_at"]

    def __str__(self):
        return f"Image for {self.car}"


class Review(models.Model):
    """Reviews for cars."""

    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="car_reviews",
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review"
        ordering = ["-created_at"]
        unique_together = ["car", "reviewer"]

    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.car}"