from django.db import models
from apps.accounts.models import CustomUser
from apps.cars.models import Car


class UserVerification(models.Model):
    """User document verification."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_verification')
    
    # Documents
    driving_license = models.FileField(upload_to='verification/driving_license/')
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    
    profile_photo = models.ImageField(upload_to='verification/profile_photos/')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='verified_users', limit_choices_to={'role': 'admin'})
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_verification'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Verification for {self.user.email}"


class CarVerification(models.Model):
    """Car document verification."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='car_verification')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='verified_cars', limit_choices_to={'role': 'admin'})
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Verification checklist
    rc_valid = models.BooleanField(default=False)
    insurance_valid = models.BooleanField(default=False)
    owner_verified = models.BooleanField(default=False)
    documents_clear = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'car_verification'
        indexes = [
            models.Index(fields=['car', 'status']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Verification for {self.car}"


class AuditLog(models.Model):
    """Audit log for admin actions."""
    
    ACTION_CHOICES = (
        ('user_verified', 'User Verified'),
        ('user_rejected', 'User Rejected'),
        ('car_verified', 'Car Verified'),
        ('car_rejected', 'Car Rejected'),
        ('user_banned', 'User Banned'),
        ('user_unbanned', 'User Unbanned'),
        ('booking_approved', 'Booking Approved'),
        ('booking_rejected', 'Booking Rejected'),
    )
    
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                             related_name='audit_logs', limit_choices_to={'role': 'admin'})
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='audit_log_targets')
    target_car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='audit_logs')
    
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_log'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['admin']),
            models.Index(fields=['action']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.action} by {self.admin.email if self.admin else 'Unknown'}"
