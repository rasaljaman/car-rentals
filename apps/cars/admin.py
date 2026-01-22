from django.contrib import admin
from django.utils.html import format_html
from apps.cars.models import Car, CarImage, Review


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ['image', 'is_primary']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner_email', 'price_per_day', 'status', 'is_available', 'rating', 'created_at']
    list_filter = ['status', 'fuel_type', 'transmission', 'is_available', 'created_at']
    search_fields = ['title', 'brand', 'model', 'owner__email', 'registration_number']
    readonly_fields = ['rating', 'total_bookings', 'created_at', 'updated_at', 'deleted_at']
    
    fieldsets = (
        ('Car Information', {
            'fields': ('owner', 'title', 'brand', 'model', 'year', 'color')
        }),
        ('Specifications', {
            'fields': ('fuel_type', 'transmission', 'seats', 'mileage')
        }),
        ('Rental Details', {
            'fields': ('price_per_day', 'location', 'description')
        }),
        ('Registration & Documents', {
            'fields': ('registration_number', 'rc_document', 'insurance_document')
        }),
        ('Status & Availability', {
            'fields': ('status', 'is_available')
        }),
        ('Ratings & Reviews', {
            'fields': ('rating', 'total_bookings'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CarImageInline]
    
    def owner_email(self, obj):
        return obj.owner.email
    owner_email.short_description = 'Owner'
    
    actions = ['approve_car', 'reject_car', 'delist_car']
    
    def approve_car(self, request, queryset):
        updated = queryset.update(status='verified')
        self.message_user(request, f'{updated} car(s) approved.')
    approve_car.short_description = 'Approve selected cars'
    
    def reject_car(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} car(s) rejected.')
    reject_car.short_description = 'Reject selected cars'
    
    def delist_car(self, request, queryset):
        updated = queryset.update(status='delisted', is_available=False)
        self.message_user(request, f'{updated} car(s) delisted.')
    delist_car.short_description = 'Delist selected cars'


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['car__title']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['car', 'reviewer_email', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['car__title', 'reviewer__email', 'comment']
    readonly_fields = ['created_at']
    
    def reviewer_email(self, obj):
        return obj.reviewer.email
    reviewer_email.short_description = 'Reviewer'
