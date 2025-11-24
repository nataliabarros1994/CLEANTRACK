"""
Custom decorators for role-based access control
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def role_required(*allowed_roles):
    """
    Decorator to restrict access to views based on user roles.
    
    Usage:
        @role_required('admin', 'manager')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    f'Acesso negado. Esta página requer permissões de: {", ".join(allowed_roles)}'
                )
                return redirect('home')
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorator to restrict access to admin users only.
    
    Usage:
        @admin_required
        def admin_dashboard(request):
            ...
    """
    return role_required('admin')(view_func)


def manager_or_admin_required(view_func):
    """
    Decorator to restrict access to managers and admins.
    
    Usage:
        @manager_or_admin_required
        def reports_view(request):
            ...
    """
    return role_required('admin', 'manager')(view_func)


def technician_or_above(view_func):
    """
    Decorator to allow access to technicians, managers, and admins.
    
    Usage:
        @technician_or_above
        def cleaning_log_form(request):
            ...
    """
    return role_required('admin', 'manager', 'technician')(view_func)
