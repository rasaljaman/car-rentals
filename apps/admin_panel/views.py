from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseForbidden
from apps.cars.models import Car, CarImage
from apps.accounts.models import CustomUser
from apps.verification.models import CarVerification
from django.views.decorators.http import require_http_methods


def is_admin(user):
    """Check if user is admin."""
    return user.is_authenticated and user.is_staff


def admin_required(view_func):
    """Decorator to protect admin views."""
    def wrapped_view(request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, 'Unauthorized access. Admin only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapped_view


@require_http_methods(["GET"])
@admin_required
def admin_dashboard(request):
    """Admin dashboard - view all cars and stats."""
    cars = Car.objects.all().order_by('-created_at')
    users = CustomUser.objects.all().count()
    pending_cars = Car.objects.filter(status='pending').count()
    verified_cars = Car.objects.filter(status='verified').count()
    
    context = {
        'cars': cars,
        'total_users': users,
        'pending_cars': pending_cars,
        'verified_cars': verified_cars,
        'total_cars': cars.count(),
    }
    
    return render(request, 'admin/dashboard.html', context)


@require_http_methods(["GET", "POST"])
@admin_required
def admin_add_car(request):
    """Admin panel - Add test cars directly."""
    if request.method == 'POST':
        # Get admin user (or use first admin)
        admin_user = CustomUser.objects.filter(is_staff=True).first()
        
        if not admin_user:
            messages.error(request, 'No admin user found.')
            return redirect('admin_dashboard')
        
        car_data = {
            'brand': request.POST.get('brand', ''),
            'model': request.POST.get('model', ''),
            'year': request.POST.get('year', 2024),
            'fuel_type': request.POST.get('fuel_type', 'petrol'),
            'transmission': request.POST.get('transmission', 'manual'),
            'seats': request.POST.get('seats', 5),
            'location': request.POST.get('location', ''),
            'price_per_day': request.POST.get('price_per_day', 0),
            'registration_number': request.POST.get('registration_number', ''),
            'is_available': True,
            'status': 'verified',  # Admin cars are auto-verified
            'owner': admin_user,
        }
        
        try:
            car = Car.objects.create(**car_data)
            
            # Auto-verify the car
            CarVerification.objects.create(
                car=car,
                status='approved',
                verified_by=admin_user
            )
            
            # Handle images if provided
            image_count = 0
            if 'images' in request.FILES:
                image_files = request.FILES.getlist('images')
                for idx, file in enumerate(image_files):
                    # Validate image file
                    if file.size > 10485760:  # 10MB limit
                        messages.warning(request, f'Image "{file.name}" exceeds 10MB limit and was skipped.')
                        continue
                    
                    if not file.content_type.startswith('image/'):
                        messages.warning(request, f'File "{file.name}" is not a valid image and was skipped.')
                        continue
                    
                    try:
                        CarImage.objects.create(
                            car=car,
                            image=file,
                            is_primary=(idx == 0 and image_count == 0)
                        )
                        image_count += 1
                    except Exception as e:
                        messages.warning(request, f'Failed to upload image "{file.name}": {str(e)}')
            
            # Build success message
            success_msg = f'Car "{car.brand} {car.model}" ({car.year}) added successfully!'
            if image_count > 0:
                success_msg += f' with {image_count} image{"s" if image_count != 1 else ""}.'
            messages.success(request, success_msg)
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error adding car: {str(e)}')
    
    context = {
        'fuel_types': Car.FUEL_TYPE_CHOICES,
        'transmissions': [('manual', 'Manual'), ('automatic', 'Automatic')],
    }
    
    return render(request, 'admin/add_car.html', context)


@require_http_methods(["POST"])
@admin_required
def admin_approve_car(request, car_id):
    """Admin approve a car."""
    car = get_object_or_404(Car, id=car_id)
    car.status = 'verified'
    car.save()
    
    # Create verification record
    CarVerification.objects.get_or_create(
        car=car,
        defaults={'status': 'approved', 'verified_by': request.user}
    )
    
    messages.success(request, f'Car approved: {car.make} {car.model}')
    return redirect('admin_dashboard')


@require_http_methods(["POST"])
@admin_required
def admin_reject_car(request, car_id):
    """Admin reject a car."""
    car = get_object_or_404(Car, id=car_id)
    car.status = 'rejected'
    car.save()
    
    messages.success(request, f'Car rejected: {car.make} {car.model}')
    return redirect('admin_dashboard')


@require_http_methods(["POST"])
@admin_required
def admin_delete_car(request, car_id):
    """Admin delete a car."""
    car = get_object_or_404(Car, id=car_id)
    car_name = f'{car.make} {car.model}'
    car.delete()
    
    messages.success(request, f'Car deleted: {car_name}')
    return redirect('admin_dashboard')


@require_http_methods(["GET"])
@admin_required
def admin_view_users(request):
    """Admin view all users."""
    users = CustomUser.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
        'total_users': users.count(),
        'verified_users': users.filter(is_verified=True).count(),
        'admin_users': users.filter(is_staff=True).count(),
    }
    
    return render(request, 'admin/view_users.html', context)
