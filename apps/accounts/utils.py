import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import OTPVerification


def generate_otp(length=6):
    """Generate a random OTP code."""
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(user_email, otp_code):
    """Send OTP via email."""
    subject = 'Your Sura Rentals OTP Code'
    message = f"""
    Hello,
    
    Your OTP code for Sura Rentals is: {otp_code}
    
    This code will expire in {settings.OTP_VALIDITY_MINUTES} minutes.
    
    If you didn't request this, please ignore this email.
    
    Best regards,
    Sura Rentals Team
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )


def send_otp_sms(phone_number, otp_code):
    """Send OTP via SMS (placeholder for SMS API integration)."""
    # This would integrate with a real SMS service like Twilio, AWS SNS, etc.
    # For now, it's a placeholder
    print(f"SMS to {phone_number}: Your OTP is {otp_code}")
    pass


def create_otp_record(user, otp_type='email'):
    """Create an OTP record for a user."""
    # Delete expired OTPs
    OTPVerification.objects.filter(user=user, otp_type=otp_type, expires_at__lt=timezone.now()).delete()
    
    # Create new OTP
    otp_code = generate_otp()
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_VALIDITY_MINUTES)
    
    otp = OTPVerification.objects.create(
        user=user,
        otp_code=otp_code,
        otp_type=otp_type,
        expires_at=expires_at
    )
    
    return otp


def verify_otp(user, otp_code, otp_type='email'):
    """Verify OTP for a user."""
    try:
        otp = OTPVerification.objects.get(
            user=user,
            otp_code=otp_code,
            otp_type=otp_type,
            is_verified=False
        )
        
        if otp.is_expired():
            return False, "OTP has expired"
        
        otp.is_verified = True
        otp.save()
        
        # Update user verification status
        if otp_type == 'email':
            user.is_email_verified = True
        elif otp_type == 'phone':
            user.is_phone_verified = True
        
        user.save()
        return True, "OTP verified successfully"
    
    except OTPVerification.DoesNotExist:
        return False, "Invalid OTP"
