from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from apps.accounts.models import CustomUser, Profile, OTPVerification, SignUpSession


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'get_full_name', 'phone_number', 'role', 'verification_status', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_email_verified', 'is_phone_verified', 'is_active', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'location')
        }),
        ('Account Status', {
            'fields': ('is_active', 'is_verified', 'is_email_verified', 'is_phone_verified', 'role')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'
    
    def verification_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        return format_html('<span style="color: orange;">⧖ Pending</span>')
    verification_status.short_description = 'Status'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(role='user')
        return qs


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'rating', 'total_rentals', 'total_listings', 'is_banned']
    list_filter = ['rating', 'is_banned', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'otp_type', 'is_verified', 'is_expired', 'expires_at']
    list_filter = ['otp_type', 'is_verified', 'expires_at']
    search_fields = ['user__email']
    readonly_fields = ['user', 'otp_code', 'created_at', 'expires_at']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(SignUpSession)
class SignUpSessionAdmin(admin.ModelAdmin):
    list_display = ['email', 'step_completed', 'email_otp_verified', 'phone_otp_verified', 'created_at']
    list_filter = ['step_completed', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Session Information', {
            'fields': ('email', 'step_completed')
        }),
        ('User Details', {
            'fields': ('first_name', 'last_name', 'phone_number', 'location')
        }),
        ('Verification Status', {
            'fields': ('email_otp_verified', 'phone_otp_verified', 'captcha_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
