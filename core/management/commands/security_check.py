from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check security settings and provide recommendations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Security Check Report ==='))
        
        # Check SECRET_KEY
        if settings.SECRET_KEY.startswith('django-insecure-'):
            self.stdout.write(
                self.style.WARNING('❌ SECRET_KEY is using default insecure value')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ SECRET_KEY is properly configured')
            )
        
        # Check DEBUG
        if settings.DEBUG:
            self.stdout.write(
                self.style.WARNING('❌ DEBUG is True - should be False in production')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ DEBUG is False')
            )
        
        # Check ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS:
            self.stdout.write(
                self.style.WARNING('❌ ALLOWED_HOSTS is empty')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✅ ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}')
            )
        
        # Check HTTPS settings
        if not settings.SECURE_SSL_REDIRECT:
            self.stdout.write(
                self.style.WARNING('❌ SECURE_SSL_REDIRECT is False')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ SECURE_SSL_REDIRECT is True')
            )
        
        # Check session security
        if not settings.SESSION_COOKIE_SECURE:
            self.stdout.write(
                self.style.WARNING('❌ SESSION_COOKIE_SECURE is False')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ SESSION_COOKIE_SECURE is True')
            )
        
        # Check CSRF security
        if not settings.CSRF_COOKIE_SECURE:
            self.stdout.write(
                self.style.WARNING('❌ CSRF_COOKIE_SECURE is False')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ CSRF_COOKIE_SECURE is True')
            )
        
        # Check HSTS
        if not settings.SECURE_HSTS_SECONDS:
            self.stdout.write(
                self.style.WARNING('❌ SECURE_HSTS_SECONDS is not set')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✅ SECURE_HSTS_SECONDS: {settings.SECURE_HSTS_SECONDS}')
            )
        
        self.stdout.write(self.style.SUCCESS('\n=== Recommendations ==='))
        self.stdout.write('1. Set DEBUG=False in production')
        self.stdout.write('2. Configure a strong SECRET_KEY')
        self.stdout.write('3. Set ALLOWED_HOSTS for your domain')
        self.stdout.write('4. Enable HTTPS redirects')
        self.stdout.write('5. Enable secure cookies')
        self.stdout.write('6. Configure HSTS headers')
        self.stdout.write('7. Use environment variables for sensitive settings') 