from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import CleaningLog, TemporaryTokenLog
from apps.equipment.models import Equipment
from apps.accounts.models import User


@admin.register(CleaningLog)
class CleaningLogAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'cleaned_by', 'cleaned_at', 'is_compliant', 'has_photo', 'created_at']
    list_filter = ['is_compliant', 'cleaned_at', 'created_at']
    search_fields = ['equipment__name', 'equipment__serial_number', 'cleaned_by__email', 'notes']
    raw_id_fields = ['equipment', 'cleaned_by']
    date_hierarchy = 'cleaned_at'
    readonly_fields = ['created_at', 'photo_preview']

    fieldsets = (
        ('Equipment & Staff', {
            'fields': ('equipment', 'cleaned_by')
        }),
        ('Cleaning Details', {
            'fields': ('cleaned_at', 'notes', 'photo', 'photo_preview', 'is_compliant')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Filter cleaning logs based on user's assigned facilities
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Filter by equipment in user's managed facilities
        return qs.filter(equipment__facility__managers=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Limit equipment and user choices to user's managed facilities
        """
        if db_field.name == "equipment" and not request.user.is_superuser:
            kwargs["queryset"] = Equipment.objects.filter(
                facility__managers=request.user
            )

        if db_field.name == "cleaned_by" and not request.user.is_superuser:
            # Show only users assigned to same facilities
            kwargs["queryset"] = User.objects.filter(
                managed_facilities__in=request.user.managed_facilities.all()
            ).distinct()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        """Technicians and managers can add cleaning logs"""
        return True  # All authenticated users can add logs

    def has_change_permission(self, request, obj=None):
        """Managers can edit, technicians have read-only"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        # Check if user has access to this log's equipment facility
        if request.user.role == 'manager':
            return obj.equipment.facility.managers.filter(id=request.user.id).exists()

        return False

    def has_delete_permission(self, request, obj=None):
        """Only managers can delete logs in their facilities"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        if request.user.role == 'manager':
            return obj.equipment.facility.managers.filter(id=request.user.id).exists()

        return False

    def save_model(self, request, obj, form, change):
        """Auto-fill cleaned_by if not set"""
        if not obj.cleaned_by and request.user.role == 'technician':
            obj.cleaned_by = request.user
        super().save_model(request, obj, form, change)

    def has_photo(self, obj):
        """Display if photo exists"""
        return bool(obj.photo)
    has_photo.boolean = True
    has_photo.short_description = 'Photo?'

    def photo_preview(self, obj):
        """Display photo preview in admin"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px;" />',
                obj.photo.url
            )
        return "No photo"
    photo_preview.short_description = 'Photo Preview'


@admin.register(TemporaryTokenLog)
class TemporaryTokenLogAdmin(admin.ModelAdmin):
    """Admin for temporary token audit logs"""
    list_display = [
        'equipment',
        'created_by',
        'created_at',
        'expires_at',
        'status_badge',
        'was_used',
        'times_accessed',
        'generated_from_ip'
    ]
    list_filter = [
        'was_used',
        'created_at',
        'expires_at',
        'expiry_minutes'
    ]
    search_fields = [
        'equipment__name',
        'equipment__serial_number',
        'created_by__email',
        'token',
        'generated_from_ip'
    ]
    readonly_fields = [
        'equipment',
        'token',
        'created_by',
        'created_at',
        'expires_at',
        'expiry_minutes',
        'was_used',
        'used_at',
        'times_accessed',
        'generated_from_ip',
        'status_display',
        'time_remaining_display',
        'token_url'
    ]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Token Information', {
            'fields': (
                'equipment',
                'token',
                'token_url',
                'status_display',
            )
        }),
        ('Timing', {
            'fields': (
                'created_at',
                'expires_at',
                'expiry_minutes',
                'time_remaining_display',
            )
        }),
        ('Usage Tracking', {
            'fields': (
                'was_used',
                'used_at',
                'times_accessed',
            )
        }),
        ('Audit', {
            'fields': (
                'created_by',
                'generated_from_ip',
            )
        }),
    )

    def has_add_permission(self, request):
        """Tokens are generated via API, not manually"""
        return False

    def has_change_permission(self, request, obj=None):
        """Read-only model"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deletion of old tokens"""
        return request.user.is_superuser

    def get_queryset(self, request):
        """Filter by user's facilities"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(equipment__facility__managers=request.user)

    def status_badge(self, obj):
        """Display token status as badge"""
        if obj.is_expired():
            return format_html(
                '<span style="padding: 3px 8px; background: #dc3545; color: white; border-radius: 3px;">🔒 Expirado</span>'
            )
        elif obj.was_used:
            return format_html(
                '<span style="padding: 3px 8px; background: #28a745; color: white; border-radius: 3px;">✅ Usado</span>'
            )
        else:
            return format_html(
                '<span style="padding: 3px 8px; background: #ffc107; color: black; border-radius: 3px;">⏳ Ativo</span>'
            )
    status_badge.short_description = 'Status'

    def status_display(self, obj):
        """Detailed status display"""
        if obj.is_expired():
            time_ago = timezone.now() - obj.expires_at
            minutes_ago = int(time_ago.total_seconds() / 60)
            return format_html(
                '<div style="padding: 10px; background: #f8d7da; border: 1px solid #dc3545; border-radius: 5px;">'
                '<strong style="color: #721c24;">🔒 Token Expirado</strong><br>'
                '<small>Expirou há {} minuto(s)</small>'
                '</div>',
                minutes_ago
            )
        elif obj.was_used:
            return format_html(
                '<div style="padding: 10px; background: #d4edda; border: 1px solid #28a745; border-radius: 5px;">'
                '<strong style="color: #155724;">✅ Token Usado</strong><br>'
                '<small>Usado em {}</small>'
                '</div>',
                obj.used_at.strftime('%d/%m/%Y %H:%M:%S') if obj.used_at else 'N/A'
            )
        else:
            remaining = obj.time_remaining()
            minutes = int(remaining.total_seconds() / 60)
            return format_html(
                '<div style="padding: 10px; background: #fff3cd; border: 1px solid #ffc107; border-radius: 5px;">'
                '<strong style="color: #856404;">⏳ Token Ativo</strong><br>'
                '<small>{} minuto(s) restantes</small>'
                '</div>',
                minutes
            )
    status_display.short_description = 'Status Detalhado'

    def time_remaining_display(self, obj):
        """Display time remaining until expiration"""
        if obj.is_expired():
            return "❌ Expirado"

        remaining = obj.time_remaining()
        minutes = int(remaining.total_seconds() / 60)
        seconds = int(remaining.total_seconds() % 60)

        return f"⏱️ {minutes}m {seconds}s"
    time_remaining_display.short_description = 'Tempo Restante'

    def token_url(self, obj):
        """Display clickable token URL"""
        url = f"http://localhost:8000/temp-log/{obj.token}/"
        return format_html(
            '<a href="{}" target="_blank" style="font-family: monospace; font-size: 12px;">{}</a><br>'
            '<button type="button" onclick="navigator.clipboard.writeText(\'{}\'); alert(\'URL copiada!\');" '
            'style="margin-top: 5px; padding: 3px 8px; background: #007bff; color: white; border: none; '
            'border-radius: 3px; cursor: pointer; font-size: 11px;">📋 Copiar URL</button>',
            url, url, url
        )
    token_url.short_description = 'URL do Token'
