from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from apps.verification.models import UserVerification, AuditLog
from django.utils import timezone


@require_http_methods(["GET", "POST"])
@login_required
def upload_verification(request):
    """Upload documents for user verification."""
    user = request.user
    
    try:
        user_verification = user.user_verification
    except UserVerification.DoesNotExist:
        user_verification = None
    
    if request.method == 'POST':
        if user_verification and user_verification.status == 'approved':
            messages.error(request, 'You are already verified.')
            return redirect('dashboard')
        
        driving_license = request.FILES.get('driving_license')
        license_number = request.POST.get('license_number')
        license_expiry_date = request.POST.get('license_expiry_date')
        profile_photo = request.FILES.get('profile_photo')
        
        if not all([driving_license, license_number, license_expiry_date, profile_photo]):
            messages.error(request, 'All fields are required.')
            return render(request, 'verification/upload.html')
        
        if user_verification:
            user_verification.driving_license = driving_license
            user_verification.license_number = license_number
            user_verification.license_expiry_date = license_expiry_date
            user_verification.profile_photo = profile_photo
            user_verification.status = 'pending'
            user_verification.save()
        else:
            user_verification = UserVerification.objects.create(
                user=user,
                driving_license=driving_license,
                license_number=license_number,
                license_expiry_date=license_expiry_date,
                profile_photo=profile_photo,
                status='pending'
            )
        
        messages.success(request, 'Documents uploaded. Awaiting admin verification.')
        return redirect('dashboard')
    
    return render(request, 'verification/upload.html', {
        'user_verification': user_verification
    })


@require_http_methods(["GET"])
@login_required
def verification_status(request):
    """Check verification status."""
    user = request.user
    
    try:
        user_verification = user.user_verification
    except UserVerification.DoesNotExist:
        user_verification = None
    
    context = {
        'user_verification': user_verification,
    }
    
    return render(request, 'verification/status.html', context)


@require_http_methods(["POST"])
@login_required
def approve_user_verification(request, user_id):
    """Admin approves user verification."""
    if not request.user.role == 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('home')
    
    try:
        user_verification = UserVerification.objects.get(user__id=user_id)
        user_verification.status = 'approved'
        user_verification.verified_by = request.user
        user_verification.verified_at = timezone.now()
        user_verification.save()
        
        # Update user verification status
        user_verification.user.is_verified = True
        user_verification.user.save()
        
        # Log action
        AuditLog.objects.create(
            admin=request.user,
            action='user_verified',
            target_user=user_verification.user,
            description=f'User {user_verification.user.email} verified'
        )
        
        messages.success(request, 'User verified.')
    except UserVerification.DoesNotExist:
        messages.error(request, 'Verification not found.')
    
    return redirect('admin:accounts_userverification_changelist')
