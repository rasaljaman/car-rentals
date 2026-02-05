from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseForbidden

from apps.cars.models import Car, CarImage, Review
from apps.accounts.forms import CarListingForm
from apps.verification.models import CarVerification
from apps.core.storage import upload_to_supabase


# ==========================================================
# PUBLIC VIEWS
# ==========================================================

@require_http_methods(["GET"])
def browse_cars(request):
    """Browse all verified cars with filters."""
    cars = Car.objects.filter(status="verified", is_available=True)

    location = request.GET.get("location", "")
    fuel_type = request.GET.get("fuel_type", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")

    if location:
        cars = cars.filter(location__icontains=location)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)

    cars = cars.order_by("-created_at")

    return render(request, "cars/browse.html", {
        "cars": cars,
        "fuel_types": Car.FUEL_TYPE_CHOICES,
        "filters": {
            "location": location,
            "fuel_type": fuel_type,
            "min_price": min_price,
            "max_price": max_price,
        }
    })


@require_http_methods(["GET"])
def car_detail(request, car_id):
    """Car detail page with images and reviews."""
    car = get_object_or_404(Car, id=car_id, status="verified")
    images = car.images.all()
    reviews = car.reviews.all()

    return render(request, "cars/detail.html", {
        "car": car,
        "images": images,
        "reviews": reviews,
        "primary_image": images.first(),
    })


# ==========================================================
# USER CAR LISTING (NORMAL USERS)
# ==========================================================

@require_http_methods(["GET", "POST"])
@login_required
def create_car_listing(request):
    """User creates a car listing (needs admin verification)."""
    user = request.user

    if not user.is_verified:
        messages.error(request, "You must be verified to list a car.")
        return redirect("upload_verification")

    if request.method == "POST":
        form = CarListingForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = user
            car.status = "pending"
            car.save()

            CarVerification.objects.create(car=car)

            # Upload images to Supabase
            for file in request.FILES.getlist("images"):
                image_url = upload_to_supabase(file, "cars")
                CarImage.objects.create(car=car, image_url=image_url)

            messages.success(request, "Car listing created. Awaiting admin verification.")
            return redirect("dashboard")
    else:
        form = CarListingForm()

    return render(request, "cars/create_listing.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def edit_car_listing(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)

    if request.method == "POST":
        form = CarListingForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Car listing updated.")
            return redirect("dashboard")
    else:
        form = CarListingForm(instance=car)

    return render(request, "cars/edit_listing.html", {
        "form": form,
        "car": car
    })


@require_http_methods(["POST"])
@login_required
def delete_car_listing(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    car.delete()
    messages.success(request, "Car listing deleted.")
    return redirect("dashboard")


# ==========================================================
# REVIEWS
# ==========================================================

@require_http_methods(["GET", "POST"])
@login_required
def add_car_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment", "")

        Review.objects.update_or_create(
            car=car,
            reviewer=request.user,
            defaults={"rating": rating, "comment": comment},
        )

        messages.success(request, "Review added successfully.")
        return redirect("car_detail", car_id=car_id)

    return render(request, "cars/add_review.html", {"car": car})


# ==========================================================
# ADMIN VIEWS (SUPABASE AUTH ONLY)
# ==========================================================

def admin_add_car(request):
    if not request.session.get("is_admin"):
        return HttpResponseForbidden("Admin access only")

    if request.method == "POST":
        car = Car.objects.create(
            title=request.POST.get("title") or request.POST.get("name"),
            brand=request.POST.get("brand"),
            model=request.POST.get("model"),
            year=int(request.POST.get("year")),   # ✅ REQUIRED
            fuel_type=request.POST.get("fuel_type"),
            price_per_day=request.POST.get("price_per_day"),
            location=request.POST.get("location"),
            registration_number=request.POST.get("registration_number"),
            mileage=request.POST.get("mileage"),
            transmission=request.POST.get("transmission"),
            seats=request.POST.get("seats"),
            color=request.POST.get("color"),
            description=request.POST.get("description", ""),
            status="verified",
            is_available=True,
        )

        # Images → Supabase
        for file in request.FILES.getlist("images"):
            image_url = upload_to_supabase(file, "cars")
            CarImage.objects.create(car=car, image_url=image_url)

        messages.success(request, "Car added successfully.")
        return redirect("/admin-dashboard/")

    return render(request, "admin/add_car.html")