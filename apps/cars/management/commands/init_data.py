from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import SiteSettings

CustomUser = get_user_model()


class Command(BaseCommand):
    help = 'Initialize database with default data'

    def handle(self, *args, **options):
        # Create default admin user if not exists
        if not CustomUser.objects.filter(role='admin').exists():
            admin = CustomUser.objects.create_superuser(
                email='admin@surarentals.com',
                password='admin@surarentals',
                first_name='Admin',
                last_name='User',
                phone_number='+911234567890',
                location='Mumbai',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user: admin@surarentals.com'))
        
        # Create default settings
        SiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'otp_validity_minutes': 10,
                'max_otp_attempts': 5,
                'captcha_enabled': True,
                'maintenance_mode': False,
            }
        )
        self.stdout.write(self.style.SUCCESS('Default settings created'))
        
        self.stdout.write(self.style.SUCCESS('Database initialization complete!'))
