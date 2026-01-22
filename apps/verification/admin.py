from django.contrib import admin
from django.utils.html import format_html
from apps.verification.models import UserVerification, CarVerification, AuditLog


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'license_number', 'status', 'verified_by_email', 'verified_at']
    list_filter = ['status', 'verified_at']
    search_fields = ['user__email', 'license_number']
    readonly_fields = ['created_at', 'updated_at', 'verified_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('License Details', {
            'fields': ('driving_license', 'license_number', 'license_expiry_date')
        }),
        ('Profile Photo', {
            'fields': ('profile_photo',)
        }),
        ('Verification Status', {
            'fields': ('status', 'rejection_reason')
        }),
        ('Verified By', {
            'fields': ('verified_by', 'verified_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_verification', 'reject_verification']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def verified_by_email(self, obj):
        return obj.verified_by.email if obj.verified_by else 'Not verified'
    verified_by_email.short_description = 'Verified By'
    
    def approve_verification(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='approved', verified_by=request.user, verified_at=timezone.now())
        for user_verif in queryset:
            user_verif.user.is_verified = True
            user_verif.user.save()
        self.message_user(request, f'{queryset.count()} user(s) verified.')
    approve_verification.short_description = 'Approve selected verifications'
    
    def reject_verification(self, request, queryset):
        queryset.update(status='rejected', verified_by=request.user)
        self.message_user(request, f'{queryset.count()} verification(s) rejected.')
    reject_verification.short_description = 'Reject selected verifications'


@admin.register(CarVerification)
class CarVerificationAdmin(admin.ModelAdmin):
    list_display = ['car_title', 'status', 'verified_by_email', 'verified_at']
    list_filter = ['status', 'rc_valid', 'insurance_valid', 'owner_verified', 'verified_at']
    search_fields = ['car__title', 'car__owner__email']
    readonly_fields = ['created_at', 'updated_at', 'verified_at']
    
    fieldsets = (
        ('Car Information', {
            'fields': ('car',)
        }),
        ('Verification Checklist', {
            'fields': ('rc_valid', 'insurance_valid', 'owner_verified', 'documents_clear')
        }),
        ('Verification Status', {
            'fields': ('status', 'rejection_reason')
        }),
        ('Verified By', {
            'fields': ('verified_by', 'verified_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_car_verification', 'reject_car_verification']
    
    def car_title(self, obj):
        return obj.car.title
    car_title.short_description = 'Car'
    
    def verified_by_email(self, obj):
        return obj.verified_by.email if obj.verified_by else 'Not verified'
    verified_by_email.short_description = 'Verified By'
    
    def approve_car_verification(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='approved', verified_by=request.user, verified_at=timezone.now())
        for car_verif in queryset:
            car_verif.car.status = 'verified'
            car_verif.car.save()
        self.message_user(request, f'{queryset.count()} car(s) verified.')
    approve_car_verification.short_description = 'Approve selected car verifications'
    
    def reject_car_verification(self, request, queryset):
        queryset.update(status='rejected', verified_by=request.user)
        for car_verif in queryset:
            car_verif.car.status = 'rejected'
            car_verif.car.save()
        self.message_user(request, f'{queryset.count()} car(s) rejected.')
    reject_car_verification.short_description = 'Reject selected car verifications'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'action', 'admin_email', 'target_email', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['admin__email', 'target_user__email', 'description']
    readonly_fields = ['admin', 'action', 'target_user', 'target_car', 'description', 'created_at']
    
    def admin_email(self, obj):
        return obj.admin.email if obj.admin else 'Unknown'
    admin_email.short_description = 'Admin'
    
    def target_email(self, obj):
        if obj.target_user:
            return obj.target_user.email
        elif obj.target_car:
            return obj.target_car.owner.email
        return '-'
    target_email.short_description = 'Target'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
