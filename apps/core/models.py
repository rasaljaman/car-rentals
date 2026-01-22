from django.db import models


class SiteSettings(models.Model):
    """Global site settings."""
    
    otp_validity_minutes = models.IntegerField(default=10)
    max_otp_attempts = models.IntegerField(default=5)
    captcha_enabled = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'site_settings'
    
    def __str__(self):
        return "Site Settings"
    
    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
