import logging
from django.http import HttpResponseForbidden
from django.conf import settings

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add security headers
        response = self.get_response(request)
        
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp_policy
        
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}

    def __call__(self, request):
        # Simple rate limiting for login attempts
        if request.path == '/login' and request.method == 'POST':
            client_ip = self.get_client_ip(request)
            if self.is_rate_limited(client_ip):
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return HttpResponseForbidden("Demasiados intentos de inicio de sesión. Inténtelo más tarde.")
        
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_rate_limited(self, client_ip):
        import time
        current_time = time.time()
        
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        # Remove old requests (older than 1 hour)
        self.request_counts[client_ip] = [
            req_time for req_time in self.request_counts[client_ip] 
            if current_time - req_time < 3600
        ]
        
        # Add current request
        self.request_counts[client_ip].append(current_time)
        
        # Check if more than 5 requests in the last hour
        return len(self.request_counts[client_ip]) > 5 