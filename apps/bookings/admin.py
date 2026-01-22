from django.contrib import admin
from apps.bookings.models import Booking, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'car_title', 'renter_email', 'owner_email', 'status', 'start_date', 'end_date', 'total_price']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['car__title', 'renter__email', 'owner__email']
    readonly_fields = ['total_days', 'total_price', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Booking Details', {
            'fields': ('car', 'renter', 'owner', 'status')
        }),
        ('Rental Period', {
            'fields': ('start_date', 'end_date', 'total_days')
        }),
        ('Pricing', {
            'fields': ('price_per_day', 'total_price')
        }),
        ('Locations', {
            'fields': ('pickup_location', 'dropoff_location')
        }),
        ('Notes', {
            'fields': ('renter_notes', 'owner_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PaymentInline]
    
    actions = ['approve_booking', 'reject_booking']
    
    def booking_id(self, obj):
        return f"#{obj.id}"
    booking_id.short_description = 'Booking'
    
    def car_title(self, obj):
        return obj.car.title
    car_title.short_description = 'Car'
    
    def renter_email(self, obj):
        return obj.renter.email
    renter_email.short_description = 'Renter'
    
    def owner_email(self, obj):
        return obj.owner.email
    owner_email.short_description = 'Owner'
    
    def approve_booking(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} booking(s) approved.')
    approve_booking.short_description = 'Approve selected bookings'
    
    def reject_booking(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} booking(s) rejected.')
    reject_booking.short_description = 'Reject selected bookings'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['booking__id', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    
    def booking_id(self, obj):
        return f"Booking #{obj.booking.id}"
    booking_id.short_description = 'Booking'
