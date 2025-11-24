"""
Authentication and user management views
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from .decorators import admin_required, manager_or_admin_required


def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate using email
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.get_full_name()}!')
                
                # Redirect based on role
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                elif user.role == 'admin':
                    return redirect('admin:index')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Sua conta está inativa.')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Main dashboard after login
    """
    from apps.equipment.models import Equipment
    from apps.cleaning_logs.models import CleaningLog
    
    # Get user's statistics
    context = {
        'user': request.user,
        'total_equipment': Equipment.objects.filter(is_active=True).count(),
        'overdue_equipment': sum(1 for eq in Equipment.objects.filter(is_active=True) if eq.is_overdue),
        'recent_cleanings': CleaningLog.objects.select_related('equipment', 'cleaned_by').order_by('-cleaned_at')[:5],
    }
    
    return render(request, 'accounts/dashboard.html', context)


@admin_required
def user_list_view(request):
    """
    List all users (admin only)
    """
    from .models import User
    
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
    }
    
    return render(request, 'accounts/user_list.html', context)


@manager_or_admin_required
def reports_view(request):
    """
    Reports page (managers and admins)
    """
    from apps.equipment.models import Equipment
    from apps.cleaning_logs.models import CleaningLog
    from django.utils import timezone
    from datetime import timedelta
    
    # Calculate statistics
    total_equipment = Equipment.objects.filter(is_active=True).count()
    overdue_count = sum(1 for eq in Equipment.objects.filter(is_active=True) if eq.is_overdue)
    
    # Last 7 days
    week_ago = timezone.now() - timedelta(days=7)
    cleanings_this_week = CleaningLog.objects.filter(cleaned_at__gte=week_ago).count()
    
    compliance_rate = ((total_equipment - overdue_count) / total_equipment * 100) if total_equipment > 0 else 0
    
    context = {
        'total_equipment': total_equipment,
        'overdue_count': overdue_count,
        'cleanings_this_week': cleanings_this_week,
        'compliance_rate': round(compliance_rate, 1),
    }
    
    return render(request, 'accounts/reports.html', context)
