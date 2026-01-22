from django.contrib import admin
from apps.core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['otp_validity_minutes', 'max_otp_attempts', 'captcha_enabled', 'maintenance_mode']
    
    fieldsets = (
        ('OTP Settings', {
            'fields': ('otp_validity_minutes', 'max_otp_attempts')
        }),
        ('Security', {
            'fields': ('captcha_enabled',)
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
