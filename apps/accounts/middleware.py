"""
Custom middleware for authentication and access control
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class RoleBasedAccessMiddleware:
    """
    Middleware to enforce role-based access control globally.
    
    Add to settings.py MIDDLEWARE:
        'apps.accounts.middleware.RoleBasedAccessMiddleware',
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that require specific roles
        self.role_urls = {
            '/admin/': ['admin'],
            '/reports/': ['admin', 'manager'],
            '/dashboard/': ['admin', 'manager', 'technician'],
        }
    
    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check role-based access for specific URLs
            for url_pattern, allowed_roles in self.role_urls.items():
                if request.path.startswith(url_pattern):
                    if request.user.role not in allowed_roles and not request.user.is_superuser:
                        messages.error(
                            request,
                            f'Acesso negado. Você não tem permissão para acessar esta página.'
                        )
                        return redirect('home')
        
        response = self.get_response(request)
        return response


class InactiveUserMiddleware:
    """
    Middleware to block inactive users from accessing the system.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that don't require active status
        self.exempt_urls = [
            '/accounts/login/',
            '/accounts/logout/',
            '/admin/login/',
        ]
    
    def __call__(self, request):
        # Check if user is authenticated but inactive
        if request.user.is_authenticated and not request.user.is_active:
            # Allow access to logout and login pages
            if not any(request.path.startswith(url) for url in self.exempt_urls):
                messages.warning(
                    request,
                    'Sua conta está inativa. Entre em contato com o administrador.'
                )
                return redirect('admin:logout')
        
        response = self.get_response(request)
        return response
