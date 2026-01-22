from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from apps.bookings.models import Booking, Payment
from apps.cars.models import Car


@require_http_methods(["GET", "POST"])
@login_required
def create_booking(request, car_id):
    """Create a booking request for a car."""
    car = get_object_or_404(Car, id=car_id, status='verified', is_available=True)
    
    # Check if user is verified
    if not request.user.is_verified:
        messages.error(request, 'You must be verified to rent a car.')
        return redirect('upload_verification')
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        pickup_location = request.POST.get('pickup_location')
        dropoff_location = request.POST.get('dropoff_location')
        renter_notes = request.POST.get('renter_notes')
        
        try:
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if end <= start:
                messages.error(request, 'End date must be after start date.')
                return redirect('car_detail', car_id=car_id)
            
            # Check for overlapping bookings
            overlapping = Booking.objects.filter(
                car=car,
                status__in=['pending', 'approved', 'active'],
                start_date__lt=end,
                end_date__gt=start
            ).exists()
            
            if overlapping:
                messages.error(request, 'Car is not available for these dates.')
                return redirect('car_detail', car_id=car_id)
            
            # Calculate total price
            total_days = (end - start).days
            total_price = car.price_per_day * total_days
            
            # Create booking
            booking = Booking.objects.create(
                car=car,
                renter=request.user,
                owner=car.owner,
                start_date=start,
                end_date=end,
                total_days=total_days,
                price_per_day=car.price_per_day,
                total_price=total_price,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                renter_notes=renter_notes,
                status='pending'
            )
            
            messages.success(request, 'Booking request created. Awaiting owner approval.')
            return redirect('booking_detail', booking_id=booking.id)
        
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    context = {
        'car': car,
        'min_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
    }
    
    return render(request, 'bookings/create.html', context)


@require_http_methods(["GET"])
@login_required
def booking_detail(request, booking_id):
    """View booking details."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permissions
    if request.user != booking.renter and request.user != booking.owner:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('dashboard')
    
    context = {
        'booking': booking,
        'payment': getattr(booking, 'payment', None),
    }
    
    return render(request, 'bookings/detail.html', context)


@require_http_methods(["POST"])
@login_required
def approve_booking(request, booking_id):
    """Owner approves a booking."""
    booking = get_object_or_404(Booking, id=booking_id, owner=request.user)
    
    if booking.status == 'pending':
        booking.status = 'approved'
        booking.save()
        
        # Create payment record
        Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            status='pending'
        )
        
        messages.success(request, 'Booking approved!')
    
    return redirect('booking_detail', booking_id=booking_id)


@require_http_methods(["POST"])
@login_required
def reject_booking(request, booking_id):
    """Owner rejects a booking."""
    booking = get_object_or_404(Booking, id=booking_id, owner=request.user)
    
    if booking.status == 'pending':
        booking.status = 'rejected'
        booking.save()
        messages.success(request, 'Booking rejected.')
    
    return redirect('booking_detail', booking_id=booking_id)


@require_http_methods(["GET"])
@login_required
def my_bookings(request):
    """View user's bookings as renter and owner."""
    user = request.user
    
    bookings_as_renter = Booking.objects.filter(renter=user).order_by('-created_at')
    bookings_as_owner = Booking.objects.filter(owner=user).order_by('-created_at')
    
    context = {
        'bookings_as_renter': bookings_as_renter,
        'bookings_as_owner': bookings_as_owner,
    }
    
    return render(request, 'bookings/my_bookings.html', context)
