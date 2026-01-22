from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from apps.cars.models import Car, CarImage, Review
from apps.accounts.forms import CarListingForm
from apps.verification.models import CarVerification


@require_http_methods(["GET"])
def browse_cars(request):
    """Browse all verified cars with filters."""
    cars = Car.objects.filter(status='verified', is_available=True)
    
    # Apply filters
    location = request.GET.get('location', '')
    fuel_type = request.GET.get('fuel_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if location:
        cars = cars.filter(location__icontains=location)
    
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    
    cars = cars.order_by('-created_at')
    
    context = {
        'cars': cars,
        'fuel_types': Car.FUEL_TYPE_CHOICES,
        'filters': {
            'location': location,
            'fuel_type': fuel_type,
            'min_price': min_price,
            'max_price': max_price,
        }
    }
    
    return render(request, 'cars/browse.html', context)


@require_http_methods(["GET"])
def car_detail(request, car_id):
    """Car detail page with images and reviews."""
    car = get_object_or_404(Car, id=car_id, status='verified')
    images = car.images.all()
    reviews = car.reviews.all()
    
    context = {
        'car': car,
        'images': images,
        'reviews': reviews,
        'primary_image': images.filter(is_primary=True).first() or images.first(),
    }
    
    return render(request, 'cars/detail.html', context)


@require_http_methods(["GET", "POST"])
@login_required
def create_car_listing(request):
    """Create a new car listing."""
    user = request.user
    
    # Check if user is verified
    if not user.is_verified:
        messages.error(request, 'You must be verified to list a car.')
        return redirect('upload_verification')
    
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = user
            car.save()
            
            # Create car verification record
            CarVerification.objects.create(car=car)
            
            # Handle multiple images
            for file in request.FILES.getlist('images'):
                CarImage.objects.create(car=car, image=file)
            
            messages.success(request, 'Car listing created! Awaiting admin verification.')
            return redirect('dashboard')
    else:
        form = CarListingForm()
    
    return render(request, 'cars/create_listing.html', {'form': form})


@require_http_methods(["GET", "POST"])
@login_required
def edit_car_listing(request, car_id):
    """Edit a car listing."""
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car listing updated.')
            return redirect('dashboard')
    else:
        form = CarListingForm(instance=car)
    
    return render(request, 'cars/edit_listing.html', {'form': form, 'car': car})


@require_http_methods(["POST"])
@login_required
def delete_car_listing(request, car_id):
    """Delete a car listing."""
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    car.delete()
    messages.success(request, 'Car listing deleted.')
    return redirect('dashboard')


@require_http_methods(["GET", "POST"])
@login_required
def add_car_review(request, car_id):
    """Add a review for a car."""
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        
        review = Review.objects.update_or_create(
            car=car,
            reviewer=request.user,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )
        
        messages.success(request, 'Review added successfully.')
        return redirect('car_detail', car_id=car_id)
    
    return render(request, 'cars/add_review.html', {'car': car})
