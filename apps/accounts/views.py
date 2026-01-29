from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import CustomUser, SignUpSession, Profile, OTPVerification
from apps.accounts.forms import SignUpStep1Form, OTPVerificationForm, LoginForm
from apps.accounts.utils import generate_otp, send_otp_email, send_otp_sms, create_otp_record, verify_otp


@require_http_methods(["GET", "POST"])
def home(request):
    """Home page with car search and featured listings."""
    from apps.cars.models import Car
    
    if request.method == 'POST':
        location = request.POST.get('location', '')
        if location:
            return redirect(f'browse_cars?location={location}')
    
    latest_cars = Car.objects.filter(status='verified', is_available=True).order_by('-created_at')[:6]
    
    return render(request, 'home.html', {
        'latest_cars': latest_cars
    })


@require_http_methods(["GET", "POST"])
def signup_step1(request):
    """First step of signup - collect user details."""
    if request.method == 'POST':
        form = SignUpStep1Form(request.POST)
        if form.is_valid():
            # Create or update signup session
            email = form.cleaned_data['email']
            
            signup_session = SignUpSession.objects.create(
                email=email,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                location=form.cleaned_data['location'],
                step_completed=1
            )
            
            # Hash password (will store properly in step 3)
            from django.contrib.auth.hashers import make_password
            signup_session.password_hash = make_password(form.cleaned_data['password'])
            signup_session.save()
            
            # Send email OTP
            otp_code = generate_otp()
            try:
                send_otp_email(email, otp_code)
                # Store OTP temporarily (in production, use cache or database)
                request.session[f'email_otp_{email}'] = otp_code
                request.session['signup_email'] = email
                
                messages.success(request, 'OTP sent to your email. Please verify.')
                return redirect('signup_step2')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')
    else:
        form = SignUpStep1Form()
    
    return render(request, 'signup/step1.html', {'form': form})


@require_http_methods(["GET", "POST"])
def signup_step2(request):
    """Second step of signup - Email OTP verification."""
    email = request.session.get('signup_email')
    
    if not email:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('signup_step1')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            stored_otp = request.session.get(f'email_otp_{email}')
            
            if otp_code == stored_otp:
                request.session[f'email_verified_{email}'] = True
                messages.success(request, 'Email verified! Now verify your phone.')
                return redirect('signup_step3')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'signup/step2.html', {'form': form, 'email': email})


@require_http_methods(["GET", "POST"])
def signup_step3(request):
    """Third step of signup - Phone OTP verification."""
    email = request.session.get('signup_email')
    email_verified = request.session.get(f'email_verified_{email}')
    
    if not email or not email_verified:
        messages.error(request, 'Please complete previous steps.')
        return redirect('signup_step1')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            stored_otp = request.session.get(f'phone_otp_{email}')
            
            if otp_code == stored_otp:
                # Create user account
                try:
                    signup_session = SignUpSession.objects.get(email=email)
                    
                    user = CustomUser.objects.create_user(
                        email=email,
                        password=signup_session.password_hash,  # This is hashed
                        first_name=signup_session.first_name,
                        last_name=signup_session.last_name,
                        phone_number=signup_session.phone_number,
                        location=signup_session.location,
                        is_email_verified=True,
                        is_phone_verified=True,
                        role='user'
                    )
                    
                    # Create user profile
                    Profile.objects.create(user=user)
                    
                    # Clean up session
                    del request.session['signup_email']
                    del request.session[f'email_otp_{email}']
                    del request.session[f'phone_otp_{email}']
                    del request.session[f'email_verified_{email}']
                    
                    # Delete signup session
                    signup_session.delete()
                    
                    # Log the user in
                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('dashboard')
                
                except Exception as e:
                    messages.error(request, f'Error creating account: {str(e)}')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        # Send SMS OTP if not already sent
        if not request.session.get(f'phone_otp_{email}'):
            signup_session = SignUpSession.objects.get(email=email)
            otp_code = generate_otp()
            send_otp_sms(signup_session.phone_number, otp_code)
            request.session[f'phone_otp_{email}'] = otp_code
            messages.info(request, 'Phone OTP sent via SMS.')
        
        form = OTPVerificationForm()
    
    return render(request, 'signup/step3.html', {'form': form, 'email': email})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Get user by email and verify password
            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    if not user.is_active:
                        messages.error(request, 'Your account has been deactivated.')
                    elif not user.is_email_verified:
                        messages.error(request, 'Please verify your email first.')
                    else:
                        login(request, user)
                        next_url = request.GET.get('next', 'dashboard')
                        return redirect(next_url)
                else:
                    messages.error(request, 'Invalid email or password.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


@require_http_methods(["POST"])
@login_required
def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@require_http_methods(["GET"])
@login_required
def dashboard(request):
    """User dashboard."""
    from apps.cars.models import Car
    from apps.bookings.models import Booking
    
    user = request.user
    my_cars = Car.objects.filter(owner=user)
    my_bookings = Booking.objects.filter(renter=user)
    
    context = {
        'my_cars': my_cars,
        'my_bookings': my_bookings,
        'pending_bookings': my_bookings.filter(status='pending').count(),
        'active_rentals': my_bookings.filter(status='active').count(),
    }
    
    return render(request, 'dashboard.html', context)


@require_http_methods(["GET", "POST"])
@login_required
def edit_profile(request):
    """Edit user profile."""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        
        user.first_name = name
        user.last_name = last_name
        user.save()
        
        profile.bio = bio
        
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard')
    
    return render(request, 'edit_profile.html', {'profile': profile})
